from pathlib import Path

import pandas as pd

from db import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def create_tables():
    """Create all application tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        sku TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        region TEXT,
        qty INTEGER,
        reorder_threshold INTEGER,
        unit_cost REAL,
        vendor_id TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        sku TEXT,
        qty INTEGER,
        revenue REAL,
        region TEXT,
        temperature REAL,
        rainfall REAL,
        humidity REAL,
        weather_condition TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS finance (
        id INTEGER PRIMARY KEY,
        sku TEXT,
        date TEXT,
        amount REAL,
        type TEXT,
        region TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        vendor_id TEXT PRIMARY KEY,
        name TEXT,
        lead_time_days INTEGER,
        unit_price REAL,
        on_time_delivery_rate REAL,
        quality_score REAL,
        avg_delay_days REAL,
        reliability_rating TEXT,
        return_acceptance_rate REAL,
        total_shipments_last_year INTEGER,
        payment_terms_days INTEGER,
        bulk_discount_percent REAL,
        min_order_qty INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT,
        vendor_id TEXT,
        recommended_qty INTEGER,
        estimated_cost REAL,
        status TEXT DEFAULT 'OPEN',
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def table_has_data(table_name: str) -> bool:
    """Return True if the table already contains records."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]

    conn.close()

    return count > 0


def load_csv(csv_file: str, table_name: str):
    """Load a CSV into a table only if it is empty."""

    if table_has_data(table_name):
        print(f"⏭️  {table_name} already contains data. Skipping...")
        return

    csv_path = DATA_DIR / csv_file

    if not csv_path.exists():
        print(f"❌ {csv_file} not found.")
        return

    df = pd.read_csv(csv_path)

    conn = get_connection()

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False,
    )

    conn.close()

    print(f"✅ Loaded {len(df)} rows into '{table_name}'")


def initialize_database():
    print("\n========== Inventra Database Initialization ==========\n")

    print("Creating database tables...")
    create_tables()
    print("✅ Tables ready.\n")

    print("Loading seed data...\n")

    load_csv("inventory.csv", "inventory")
    load_csv("sales.csv", "sales")
    load_csv("finance.csv", "finance")
    load_csv("vendors.csv", "vendors")

    print("\n🎉 Database initialization completed successfully!\n")


if __name__ == "__main__":
    initialize_database()