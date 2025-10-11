from pydantic import BaseModel
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# ------------------------
# USER MODELS
# ------------------------
class UserBase(BaseModel):
    """Base model for user data"""
    username: str
    email: str    
    first_name: str 
    last_name: str   
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(UserBase):
    """Model for creating a user, includes password fields"""
    email_confirm: str
    password: str       # Password is required for creation but not returned        
    confirm_password: str



class User(UserBase):
    """User model with ID"""
    id: str

    class Config:
        from_attributes = True  # For Pydantic v2


class LoginRequest(BaseModel):
    """User login request"""
    username: str      # or email if you prefer
    email: Optional[str] = None
    password: str


# ------------------------
# ITEM MODELS
# ------------------------
class ItemBase(BaseModel):
    """Base model for item data"""
    item_description: str
    directions: str
    dropoff_location: str
    contact: Optional[str] = None


class ItemCreate(ItemBase):
    """Model for creating an item"""
    pass


class Item(ItemBase):
    """Item model with private ID"""
    private_id: str

    class Config:
        from_attributes = True  # For Pydantic v2


class ItemPublic(BaseModel):
    """Public-facing item model"""
    public_id: str
    item_description: str
    directions: str
    dropoff_location: str
    contact: str = "N/A"  # default if not provided

    class Config:
        from_attributes = True


# ------------------------
# SETTINGS
# ------------------------
class Settings(BaseSettings):
    """Application settings loaded from .env"""
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
