import pandas as pd
from database.db import DBService


class InventoryService:
    """Service responsible for all inventory-related operations and analytics."""

    @staticmethod
    def get_all_products() -> list[dict]:
        """Fetch all products from inventory."""
        return DBService.query("SELECT * FROM inventory ORDER BY sku")

    @staticmethod
    def get_all_products_df() -> pd.DataFrame:
        """Fetch all inventory products as a Pandas DataFrame."""
        return DBService.query_df("SELECT * FROM inventory ORDER BY sku")

    @staticmethod
    def get_product(sku: str) -> dict | None:
        """Fetch a single product by SKU. Normalises input: 'SKU-001' → 'SKU001'."""
        sku_clean = sku.upper().replace("-", "").strip()
        return DBService.query_one("SELECT * FROM inventory WHERE sku = ?", (sku_clean,))

    @staticmethod
    def get_products_by_region(region: str) -> list[dict]:
        """Fetch all inventory items for a region."""
        return DBService.query("SELECT * FROM inventory WHERE LOWER(region) = LOWER(?) ORDER BY sku", (region,))

    @staticmethod
    def get_inventory_by_region(region: str) -> list[dict]:
        """Alias for get_products_by_region."""
        return InventoryService.get_products_by_region(region)

    @staticmethod
    def get_inventory_by_name(name: str) -> dict | None:
        """Fetch inventory item by product name."""
        return DBService.query_one("SELECT * FROM inventory WHERE LOWER(name) = LOWER(?)", (name,))

    @staticmethod
    def search_inventory(keyword: str) -> list[dict]:
        """Search inventory by keyword across name, category, or region with automatic query cleaning."""
        if not keyword:
            return InventoryService.get_all_products()

        clean_kw = keyword.lower()
        for filler in ["region", "zone", "area", "category", "products", "items"]:
            clean_kw = clean_kw.replace(filler, "")
        clean_kw = clean_kw.strip()

        pattern_raw = f"%{keyword.strip()}%"
        pattern_clean = f"%{clean_kw}%" if clean_kw else pattern_raw

        sql = """
            SELECT * FROM inventory
            WHERE LOWER(name) LIKE LOWER(?)
               OR LOWER(category) LIKE LOWER(?)
               OR LOWER(region) LIKE LOWER(?)
               OR LOWER(name) LIKE LOWER(?)
               OR LOWER(category) LIKE LOWER(?)
               OR LOWER(region) LIKE LOWER(?)
            ORDER BY sku
        """
        return DBService.query(sql, (pattern_raw, pattern_raw, pattern_raw, pattern_clean, pattern_clean, pattern_clean))


    @staticmethod
    def get_inventory_by_category(category: str) -> list[dict]:
        """Get inventory for a category."""
        return DBService.query("SELECT * FROM inventory WHERE LOWER(category) = LOWER(?)", (category,))

    @staticmethod
    def get_low_stock_products() -> list[dict]:
        """Return products below or at reorder threshold."""
        return DBService.query("SELECT * FROM inventory WHERE qty <= reorder_threshold ORDER BY qty ASC")

    @staticmethod
    def get_low_stock_df() -> pd.DataFrame:
        """Return low stock items as an enriched Pandas DataFrame with calculated metrics."""
        df = DBService.query_df("SELECT * FROM inventory WHERE qty <= reorder_threshold ORDER BY qty ASC")
        if not df.empty:
            df["total_stock_value"] = df["qty"] * df["unit_cost"]
            df["shortage_units"] = df["reorder_threshold"] - df["qty"]
            df["health_status"] = df.apply(
                lambda row: "Critical" if row["qty"] <= row["reorder_threshold"] * 0.5 else "Low",
                axis=1
            )
        return df

    @staticmethod
    def update_stock(sku: str, quantity: int):
        """Update current stock quantity."""
        sku_clean = sku.upper().replace("-", "").strip()
        DBService.execute("UPDATE inventory SET qty = ? WHERE sku = ?", (quantity, sku_clean))

    @staticmethod
    def get_product_count() -> int:
        """Return total number of products."""
        res = DBService.query_one("SELECT COUNT(*) as count FROM inventory")
        return res["count"] if res else 0