from graph.state import AgentState
from mcp_server.client import call_tool


def ticket_agent(state: AgentState):

    decision = state.get("decision")

    if not decision["reorder"]:
        return {
            "ticket": {
                "created": False,
                "reason": "Reorder not required"
            }
        }

    inventory = state["inventory_data"]

    ticket = call_tool(
        "create_ticket",
        {
            "sku": inventory["sku"],
            "qty": decision["recommended_qty"],
            "reason": decision["reason"],
        },
    )

    return {
        "ticket": ticket,
    }