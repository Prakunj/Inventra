from pydantic import BaseModel


class QueryExtraction(BaseModel):
    intent: str
    entity: str


DATA_PROMPT = """
You are an Inventory AI assistant.

Extract the following:

1. intent
2. entity

Valid intents:

- reorder
- inventory_lookup
- vendor_lookup
- weather_inventory
- low_stock
- category_lookup
- region_lookup

RULES FOR INTENT:
- 'reorder': Use whenever the user asks to reorder, check if reorder is needed, decide on stock replenishment, or evaluate purchasing for a product/SKU — EVEN IF weather, rain, temperature, or vendor lead time is mentioned in the query.
- 'weather_inventory': Use ONLY for general weather status queries for a region without a specific product reorder decision.

RULES FOR CONVERSATION HISTORY & PRONOUN RESOLUTION:
- If the user uses pronouns or references like 'it', 'that item', 'this product', 'reorder it', or 'who supplies it', look at the Recent Conversation History to find the specific SKU or Product Name being discussed and extract it as the 'entity'.


Examples:

User:
Heavy rain and humidity are forecasted for the North region. Check stock for Instant Water Heater (SKU029) and decide if we need an urgent reorder considering vendor lead time

Output:
{
"intent":"reorder",
"entity":"SKU029"
}

User:
Should I reorder SKU001?

Output:
{
"intent":"reorder",
"entity":"SKU001"
}

User:
based on north region, give product details

Output:
{
"intent":"region_lookup",
"entity":"North"
}

User:
Should I reorder Mixer Grinder?

Output:
{
"intent":"reorder",
"entity":"Mixer Grinder"
}

User:
Who supplies Mixer Grinder?

Output:
{
"intent":"vendor_lookup",
"entity":"Mixer Grinder"
}

User:
Show all low stock products

Output:
{
"intent":"low_stock",
"entity":""
}

Return ONLY JSON.
"""