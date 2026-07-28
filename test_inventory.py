from mcp_server.client import call_tool

result = call_tool(
    "get_product",
    {"sku": "SKU001"}
)

print(result)