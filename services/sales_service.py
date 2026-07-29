import pandas as pd
from database.db import DBService


class SalesService:
    """Service responsible for sales analytics, demand analysis, and weather-sales correlation using Pandas."""

    @staticmethod
    def get_sales_by_sku(sku: str) -> pd.DataFrame:
        """Fetch sales history for a SKU as a Pandas DataFrame."""
        sku_clean = sku.upper().replace("-", "").strip()
        sql = "SELECT * FROM sales WHERE sku = ? ORDER BY date DESC"
        return DBService.query_df(sql, (sku_clean,))

    @staticmethod
    def get_regional_sales_summary() -> pd.DataFrame:
        """Calculate total sales volume and revenue by region using Pandas."""
        df = DBService.query_df("SELECT region, qty, revenue FROM sales")
        if df.empty:
            return pd.DataFrame()
        summary = df.groupby("region").agg(
            total_qty=("qty", "sum"),
            total_revenue=("revenue", "sum"),
            avg_order_size=("qty", "mean")
        ).reset_index()
        return summary

    @staticmethod
    def get_weather_sales_correlation(region: str | None = None) -> pd.DataFrame:
        """Analyze sales volume vs weather conditions using Pandas aggregation."""
        if region:
            sql = "SELECT weather_condition, qty, revenue FROM sales WHERE LOWER(region) = LOWER(?)"
            df = DBService.query_df(sql, (region,))
        else:
            sql = "SELECT weather_condition, qty, revenue FROM sales"
            df = DBService.query_df(sql)

        if df.empty:
            return pd.DataFrame()

        summary = df.groupby("weather_condition").agg(
            total_units_sold=("qty", "sum"),
            total_revenue=("revenue", "sum"),
            avg_units_per_day=("qty", "mean")
        ).reset_index()
        return summary
