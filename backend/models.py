# backend/models.py
import secrets
from sqlalchemy import Column, String
from .database import Base

def generate_secure_id():
    return secrets.token_hex(8)  # 16-character hex string

class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, default=generate_secure_id)
    item_description = Column(String, nullable=False)
    directions = Column(String, nullable=False)
    dropoff_location = Column(String, nullable=False)
    contact = Column(String, nullable=True, default="N/A")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_secure_id)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name  = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(bool, default=False)
    is_superuser = Column(bool, default=False)
    is_verified = Column(bool, default=False)
