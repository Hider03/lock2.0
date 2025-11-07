# backend/models.py
import secrets
from sqlalchemy import (
    Boolean, Column, String, ForeignKey, DateTime, Text, Table
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


def generate_secure_id():
    return secrets.token_hex(8)

conversation_participants = Table(
    "conversation_participants",
    Base.metadata,
    Column("conversation_id", String, ForeignKey("conversations.id")),
    Column("user_id", String, ForeignKey("users.id")),
)

# -------------------------------
# USER MODEL
# -------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_secure_id)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="sender")

    # ✅ FIXED: use back_populates, not backref
    conversations = relationship(
        "Conversation",
        secondary=conversation_participants,
        back_populates="participants"
    )

#-------------------------------
# GUEST MODEL
#-------------------------------
class Finder(Base):
    __tablename__ = "finders"

    id = Column(String, primary_key=True, default=generate_secure_id)
    contact = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    messages = relationship("Message", back_populates="finder")




# -------------------------------
# ITEM MODEL (unchanged)
# -------------------------------
class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, default=generate_secure_id)
    item_description = Column(String, nullable=False)
    directions = Column(String, nullable=False)
    dropoff_location = Column(String, nullable=False)
    contact = Column(String, nullable=True, default="N/A")
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="items")


# -------------------------------
# CONVERSATION MODEL
# -------------------------------

# Many-to-many relationship between users and conversations

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=generate_secure_id)
    finder_id = Column(String, ForeignKey("finders.id"), nullable=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    participants = relationship(
        "User",
        secondary=conversation_participants,
        back_populates="conversations"
    )
    finder = relationship("Finder")
    
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")




# -------------------------------
# MESSAGE MODEL
# -------------------------------
class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_secure_id)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(String, ForeignKey("users.id"), nullable=True)  # ✅ make nullable, because finder may send
    finder_id = Column(String, ForeignKey("finders.id"), nullable=True)  # ✅ NEW: finder link
    message_content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", back_populates="messages")
    finder = relationship("Finder", back_populates="messages")  # ✅ NEW
