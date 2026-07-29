import pandas as pd
from database.db import DBService


class VendorService:
    """Service responsible for vendor-related operations and performance analytics."""

    @staticmethod
    def get_all_vendors() -> list[dict]:
        """Fetch all vendors."""
        return DBService.query("SELECT * FROM vendors ORDER BY vendor_id")

    @staticmethod
    def get_all_vendors_df() -> pd.DataFrame:
        """Fetch all vendors as a Pandas DataFrame."""
        return DBService.query_df("SELECT * FROM vendors ORDER BY vendor_id")

    @staticmethod
    def get_vendor(vendor_id: str) -> dict | None:
        """Fetch vendor by vendor ID."""
        return DBService.query_one("SELECT * FROM vendors WHERE vendor_id = ?", (vendor_id,))

    @staticmethod
    def get_vendor_by_sku(sku: str) -> dict | None:
        """Returns vendor details for a given SKU."""
        sku_clean = sku.upper().replace("-", "").strip()
        sql = """
            SELECT v.*
            FROM inventory i
            JOIN vendors v ON i.vendor_id = v.vendor_id
            WHERE i.sku = ?
        """
        return DBService.query_one(sql, (sku_clean,))

    @staticmethod
    def get_top_vendors(limit: int = 5) -> list[dict]:
        """Return top performing vendors sorted by on-time delivery rate and quality score."""
        sql = """
            SELECT * FROM vendors
            ORDER BY on_time_delivery_rate DESC, quality_score DESC
            LIMIT ?
        """
        return DBService.query(sql, (limit,))