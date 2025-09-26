from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class UserCreate(UserBase):
    password: str       # Password is required for creation but not returned        
    confirm_password: str

class User(UserBase):
    id: str

    class Config:
        from_attributes = True  # for Pydantic v2

        
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
