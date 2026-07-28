from graph.workflow import build_graph

graph = build_graph()

state = {
    "user_query": "Should i reorder SKU001 based on coming weather"
}

result = graph.invoke(state)
print(state["user_query"])

print("=" * 80)
print("Intent")
print(result.get("intent"))

print("=" * 80)
print("Entity")
print(result.get("entity"))

print("=" * 80)
print("Inventory")
print(result.get("inventory_data"))

print("=" * 80)
print("Vendor")
print(result.get("vendor_data"))

print("=" * 80)
print("Weather")
print(result.get("weather_data"))

print("=" * 80)
print("Decision")
print(result.get("decision"))

print("=" * 80)
print("Ticket")
print(result.get("ticket"))

print("=" * 80)
print("Report")
print(result.get("report")[0]["text"])