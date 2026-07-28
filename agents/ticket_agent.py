from graph.state import AgentState
from services.inventory_service import InventoryService
from services.ticket_service import TicketService


def ticket_agent(state: AgentState):

    decision = state.get("decision")

    if not decision or not decision["reorder"]:
        return {
            "ticket": {
                "created": False,
                "reason":  "Reorder not required",
            }
        }

    inventory = state["inventory_data"]
    vendor    = state.get("vendor_data") or {}

    vendor_id       = inventory.get("vendor_id", vendor.get("vendor_id", "UNKNOWN"))
    recommended_qty = decision["recommended_qty"]
    estimated_cost  = round(recommended_qty * inventory.get("unit_cost", 0), 2)

    ticket_id = TicketService.create_ticket(
        sku=inventory["sku"],
        vendor_id=vendor_id,
        recommended_qty=recommended_qty,
        estimated_cost=estimated_cost,
        reason=decision["reason"],
    )

    return {
        "ticket": {
            "created":         True,
            "ticket_id":       ticket_id,
            "sku":             inventory["sku"],
            "vendor_id":       vendor_id,
            "recommended_qty": recommended_qty,
            "estimated_cost":  estimated_cost,
            "status":          "OPEN",
            "reason":          decision["reason"],
        }
    }