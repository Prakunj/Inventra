from utils.config import *
from langchain_google_genai import ChatGoogleGenerativeAI

from graph.state import AgentState
from prompts.data_prompt import DATA_PROMPT, QueryExtraction
from mcp_server.client import call_tool



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
    vendor = None
    weather = None

    # -----------------------------
    # REORDER
    # -----------------------------

    if intent == "reorder":

        if entity.upper().startswith("SKU"):

            inventory = call_tool(
                "get_product",
                {"sku": entity},
            )

        else:

            inventory = call_tool(
                "get_inventory_by_name",
                {"name": entity},
            )

        inventory = inventory

        vendor = call_tool(
            "get_vendor",
            {
                "vendor_id": inventory["vendor_id"]
            },
        )

        weather = call_tool(
            "get_weather",
            {
                "region": inventory["region"]
            },
        )

        vendor = vendor
        weather = weather

    # -----------------------------
    # LOW STOCK
    # -----------------------------

    elif intent == "low_stock":

        inventory = call_tool(
            "get_low_stock_products",
            {},
        )

        inventory = inventory

    # -----------------------------
    # INVENTORY LOOKUP
    # -----------------------------

    elif intent == "inventory_lookup":

        inventory = call_tool(
            "search_inventory",
            {
                "keyword": entity
            },
        )

        inventory = inventory

    # -----------------------------
    # CATEGORY LOOKUP
    # -----------------------------

    elif intent == "category_lookup":

        inventory = call_tool(
            "get_inventory_by_category",
            {
                "category": entity
            },
        )

        inventory = inventory

    # -----------------------------
    # WEATHER
    # -----------------------------

    elif intent == "weather_inventory":

        weather = call_tool(
            "get_weather",
            {
                "region": 'North'
            },
        )

        inventory = call_tool(
            "get_inventory_by_region",
            {"region": 'North'},
        )

        weather = weather
        inventory = inventory

    return {

        **state,

        "intent": intent,

        "entity": entity,

        "inventory_data": inventory,

        "vendor_data": vendor,

        "weather_data": weather,
    }