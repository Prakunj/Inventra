import pandas as pd
from database.db import DBService


class TicketService:
    """Service responsible for managing reorder tickets and ticket analytics."""

    @staticmethod
    def create_ticket(
        sku: str,
        vendor_id: str,
        recommended_qty: int,
        estimated_cost: float,
        reason: str,
    ) -> int:
        """Create a new purchase recommendation ticket and return ticket_id."""
        sku_clean = sku.upper().replace("-", "").strip()
        sql = """
            INSERT INTO tickets (
                sku, vendor_id, recommended_qty, estimated_cost, reason
            ) VALUES (?, ?, ?, ?, ?)
        """
        return DBService.execute(sql, (sku_clean, vendor_id, recommended_qty, estimated_cost, reason))

    @staticmethod
    def get_all_tickets() -> list[dict]:
        """Fetch all tickets ordered by created_at DESC."""
        return DBService.query("SELECT * FROM tickets ORDER BY created_at DESC")

    @staticmethod
    def get_tickets_df() -> pd.DataFrame:
        """Fetch all tickets as a Pandas DataFrame."""
        return DBService.query_df("SELECT * FROM tickets ORDER BY created_at DESC")

    @staticmethod
    def get_ticket(ticket_id: int) -> dict | None:
        """Fetch a specific ticket by ID."""
        return DBService.query_one("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))

    @staticmethod
    def update_status(ticket_id: int, status: str):
        """Update ticket status (e.g. OPEN, APPROVED, CLOSED)."""
        DBService.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (status, ticket_id))