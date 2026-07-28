from database.db import get_connection


class VendorService:
    """Service responsible for vendor-related operations."""

    @staticmethod
    def get_all_vendors():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM vendors
            ORDER BY vendor_id
        """)

        vendors = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return vendors

    @staticmethod
    def get_vendor(vendor_id: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM vendors
            WHERE vendor_id = ?
        """, (vendor_id,))

        vendor = cursor.fetchone()

        conn.close()

        return dict(vendor) if vendor else None

    @staticmethod
    def get_vendor_by_sku(sku: str):
        """
        Returns vendor details for a given SKU.
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v.*
            FROM inventory i
            JOIN vendors v
            ON i.vendor_id = v.vendor_id
            WHERE i.sku = ?
        """, (sku,))

        vendor = cursor.fetchone()

        conn.close()

        return dict(vendor) if vendor else None