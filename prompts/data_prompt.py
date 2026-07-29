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

Examples:

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