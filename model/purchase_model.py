from datetime import datetime
from typing import Tuple

from bson import ObjectId
from pydantic import BaseModel, Field


class Purchase(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: ObjectId = Field(default_factory=ObjectId, alias='_id')
    user_uuid: str
    operator: str
    product_name: str
    value_month: float
    total_price: float
    installments: Tuple[int, int]
    ratio: float
    bought_at: datetime
