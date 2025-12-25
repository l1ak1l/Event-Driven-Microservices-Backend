from typing import Optional
from sqlmodel import SQLModel, Field

class Inventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: str
    quantity: int
