from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    item_description: str
    directions: str
    dropoff_location: str
    contact: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str

    class Config:
        from_attributes = True  # for Pydantic v2

class ItemResponse(BaseModel):
    id: str
    directions: str
    dropoff_location: str
    contact: Optional[str] = None

    class Config:
        from_attributes = True
