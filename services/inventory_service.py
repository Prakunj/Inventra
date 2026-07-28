from database.db import get_connection


class InventoryService:
    """Service responsible for all inventory-related database operations."""

    @staticmethod
    def get_all_products():
        """
        Fetch all products from inventory.

        Returns:
            list[dict]: List of inventory items.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM inventory
            ORDER BY sku
        """)

        products = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return products

    @staticmethod
    def get_product(sku: str):
        """
        Fetch a single product by SKU.
        Normalises input: 'SKU-001', 'sku-001', 'SKU001' → 'SKU001'
        """
        sku = sku.upper().replace("-", "").strip()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM inventory
            WHERE sku = ?
        """, (sku,))

        product = cursor.fetchone()

        conn.close()

        return dict(product) if product else None

    @staticmethod
    def get_products_by_region(region: str):
        """
        Fetch all inventory items for a region.

        Args:
            region (str): Region name.

        Returns:
            list[dict]
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM inventory
            WHERE region = ?
            ORDER BY sku
        """, (region,))

        products = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return products

    @staticmethod
    def update_stock(sku: str, quantity: int):
        """
        Update current stock quantity.

        Args:
            sku (str): Product SKU.
            quantity (int): New quantity.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE inventory
            SET qty = ?
            WHERE sku = ?
        """, (quantity, sku))

        conn.commit()
        conn.close()

    @staticmethod
    def get_product_count():
        """
        Return total number of products.

        Returns:
            int
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM inventory
        """)

        count = cursor.fetchone()[0]

        conn.close()

        return count



    @staticmethod
    def get_inventory_by_name(name: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM inventory
            WHERE LOWER(name) = LOWER(?)
        """, (name,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None


    @staticmethod
    def search_inventory(keyword: str):
        conn = get_connection()
        cursor = conn.cursor()

        keyword = f"%{keyword}%"

        cursor.execute("""
            SELECT *
            FROM inventory
            WHERE
                LOWER(name) LIKE LOWER(?)
                OR LOWER(category) LIKE LOWER(?)
                OR LOWER(region) LIKE LOWER(?)
        """, (keyword, keyword, keyword))

        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]


    @staticmethod
    def get_inventory_by_category(category: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM inventory
            WHERE LOWER(category)=LOWER(?)
        """, (category,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]


    @staticmethod
    def get_inventory_by_region(region: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM inventory
            WHERE LOWER(region)=LOWER(?)
        """, (region,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]


    @staticmethod
    def get_low_stock_products():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM inventory
        WHERE qty <= reorder_threshold
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]    