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


from utils.logger import log_llm_request, log_llm_response


def data_agent(state: AgentState):

    query = state["user_query"]
    history = state.get("chat_history") or []

    history_text = ""
    if history:
        turns = []
        for m in history[-6:]:  # Last 6 messages
            role = "USER" if m.get("role") == "user" else "ASSISTANT"
            content = m.get("content") or (m.get("state", {}).get("report", "")[:150] if isinstance(m.get("state"), dict) else "")
            if content:
                turns.append(f"{role}: {content}")
        if turns:
            history_text = "\n\nRecent Conversation History:\n" + "\n".join(turns)

    full_prompt = DATA_PROMPT + history_text + "\n\nUser Query:\n" + query

    log_llm_request("Data Agent", full_prompt)
    extraction = structured_llm.invoke(full_prompt)


    intent = extraction.intent
    entity = extraction.entity

    log_llm_response("Data Agent", f"Intent: {intent} | Entity: {entity}")


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
        requested_region = None
        for r in ["North", "South", "East", "West"]:
            if r.lower() in (entity or "").lower() or r.lower() in query.lower():
                requested_region = r
                break

        if requested_region:
            inventory = InventoryService.get_inventory_by_region(requested_region)
        else:
            inventory = InventoryService.get_products_sorted_by_region()


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