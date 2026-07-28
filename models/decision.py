from pydantic import BaseModel


class Decision(BaseModel):
    reorder: bool
    recommended_qty: int
    reason: str