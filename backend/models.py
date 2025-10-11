# backend/models.py
import secrets
from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

def generate_secure_id():
    return secrets.token_hex(8)  # 16-character hex string

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_secure_id)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name  = Column(String, nullable=False)
    last_name   = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active   = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified  = Column(Boolean, default=False)

    # ✅ Relationship to items
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"

    private_id = Column(String, primary_key=True, default=generate_secure_id)
    public_id  = Column(String, unique=True, index=True, default=generate_secure_id)
    # you can remove the public id and use the private one
    item_description = Column(String, nullable=False)
    directions       = Column(String, nullable=False)
    dropoff_location = Column(String, nullable=False)
    contact          = Column(String, nullable=True, default="N/A")

    # ✅ Foreign key to User.id
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    # ✅ Relationship back to owner
    owner = relationship("User", back_populates="items")
