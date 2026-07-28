from pathlib import Path
import sys

# Ensure project root is available for imports when running via FastMCP CLI
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastmcp import FastMCP

from services.inventory_service import InventoryService
from services.vendor_service import VendorService
from services.ticket_service import TicketService
from services.weather_service import WeatherService

mcp = FastMCP("Inventra MCP Server")


# -------------------------
# Inventory Tools
# -------------------------

@mcp.tool
def get_inventory():
    """Return all inventory products."""
    return InventoryService.get_all_products()


@mcp.tool
def get_product(sku: str):
    """Return inventory details for a SKU."""
    return InventoryService.get_product(sku)

@mcp.tool
def get_inventory_by_name(name: str):
    """
    Return inventory for a product name.
    """
    return InventoryService.get_inventory_by_name(name)


@mcp.tool
def search_inventory(keyword: str):
    """
    Search inventory by keyword.
    """
    return InventoryService.search_inventory(keyword)


@mcp.tool
def get_inventory_by_category(category: str):
    """
    Get inventory for a category.
    """
    return InventoryService.get_inventory_by_category(category) 

@mcp.tool
def get_low_stock_products():
    """
    Return products below reorder threshold.
    """
    return InventoryService.get_low_stock_products()   


# -------------------------
# Vendor Tools
# -------------------------

@mcp.tool
def get_vendor(vendor_id: str):
    """Return vendor details."""
    return VendorService.get_vendor(vendor_id)


@mcp.tool
def get_vendor_by_sku(sku: str):
    """Return vendor supplying the given SKU."""
    return VendorService.get_vendor_by_sku(sku)


# -------------------------
# Weather Tools
# -------------------------

@mcp.tool
def get_weather(region: str):
    """Return weather forecast for a region."""
    return WeatherService.get_weather(region)

@mcp.tool
def get_inventory_by_region(region: str):
    """
    Return all inventory in a region.
    """
    return InventoryService.get_inventory_by_region(region)


# -------------------------
# Ticket Tools
# -------------------------

@mcp.tool
def create_ticket(
    sku: str,
    vendor_id: str,
    recommended_qty: int,
    estimated_cost: float,
    reason: str,
):
    """Create a purchase recommendation ticket."""

    return TicketService.create_ticket(
        sku=sku,
        vendor_id=vendor_id,
        recommended_qty=recommended_qty,
        estimated_cost=estimated_cost,
        reason=reason,
    )


if __name__ == "__main__":
    mcp.run()