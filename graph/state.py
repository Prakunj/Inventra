from typing import TypedDict


class AgentState(TypedDict, total=False):

    user_query: str

    intent: str

    entity: str

    inventory_data: dict

    vendor_data: dict

    weather_data: dict

    decision: dict

    ticket: dict

    report: str