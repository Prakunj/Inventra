from utils.config import *
from langchain_google_genai import ChatGoogleGenerativeAI

from graph.state import AgentState
from prompts.data_prompt import DATA_PROMPT, QueryExtraction
from services.inventory_service import InventoryService
from services.vendor_service import VendorService
from services.weather_service import WeatherService


llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0,
)

structured_llm = llm.with_structured_output(QueryExtraction)


def data_agent(state: AgentState):

    query = state["user_query"]

    extraction = structured_llm.invoke(
        DATA_PROMPT + "\n\nUser Query:\n" + query
    )

    intent = extraction.intent
    entity = extraction.entity

    print("=" * 50)
    print("Intent:", intent)
    print("Entity:", entity)
    print("=" * 50)

    inventory = None
    vendor    = None
    weather   = None

    # -----------------------------
    # REORDER
    # -----------------------------

    if intent == "reorder":

        if entity.upper().startswith("SKU"):
            inventory = InventoryService.get_product(entity)
        else:
            inventory = InventoryService.get_inventory_by_name(entity)

        if inventory is None:
            raise ValueError(
                f"Product not found: '{entity}'. "
                "Please check the SKU or product name and try again."
            )

        vendor  = VendorService.get_vendor(inventory["vendor_id"])
        weather = WeatherService.get_weather(inventory["region"])

    # -----------------------------
    # LOW STOCK
    # -----------------------------

    elif intent == "low_stock":
        inventory = InventoryService.get_low_stock_products()

    # -----------------------------
    # INVENTORY LOOKUP
    # -----------------------------

    elif intent == "inventory_lookup":
        inventory = InventoryService.search_inventory(entity)

    # -----------------------------
    # CATEGORY LOOKUP
    # -----------------------------

    elif intent == "category_lookup":
        inventory = InventoryService.get_inventory_by_category(entity)

    # -----------------------------
    # REGION LOOKUP
    # -----------------------------

    elif intent in ["region_lookup", "region"]:
        clean_region = entity.lower().replace("region", "").strip().title() if entity else "North"
        if clean_region not in ["North", "South", "East", "West"]:
            clean_region = "North"
        inventory = InventoryService.get_inventory_by_region(clean_region)

    # -----------------------------
    # WEATHER + REGION
    # -----------------------------

    elif intent == "weather_inventory":
        weather   = WeatherService.get_weather("North")
        inventory = InventoryService.get_inventory_by_region("North")


    return {
        **state,
        "intent":         intent,
        "entity":         entity,
        "inventory_data": inventory,
        "vendor_data":    vendor,
        "weather_data":   weather,
    }