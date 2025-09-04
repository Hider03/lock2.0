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
