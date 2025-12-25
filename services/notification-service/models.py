from typing import Optional
from sqlmodel import SQLModel, Field

class NotificationLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int
    content: str
