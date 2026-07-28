from database.db import get_connection


class TicketService:
    """Service responsible for managing reorder tickets."""

    @staticmethod
    def create_ticket(
        sku: str,
        vendor_id: str,
        recommended_qty: int,
        estimated_cost: float,
        reason: str,
    ):
        """
        Create a new reorder ticket.
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tickets (
                sku,
                vendor_id,
                recommended_qty,
                estimated_cost,
                reason
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            sku,
            vendor_id,
            recommended_qty,
            estimated_cost,
            reason,
        ))

        conn.commit()

        ticket_id = cursor.lastrowid

        conn.close()

        return ticket_id

    @staticmethod
    def get_all_tickets():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tickets
            ORDER BY created_at DESC
        """)

        tickets = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return tickets

    @staticmethod
    def get_ticket(ticket_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tickets
            WHERE ticket_id = ?
        """, (ticket_id,))

        ticket = cursor.fetchone()

        conn.close()

        return dict(ticket) if ticket else None

    @staticmethod
    def update_status(ticket_id: int, status: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tickets
            SET status = ?
            WHERE ticket_id = ?
        """, (status, ticket_id))

        conn.commit()
        conn.close()