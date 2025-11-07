from sqlalchemy.orm import Session
from .models import Finder, Item
import secrets

def create_item(db: Session, item_description, directions, dropoff_location, contact, user_id):
    from .models import Item
    new_item = Item(
        item_description=item_description,
        directions=directions,
        dropoff_location=dropoff_location,
        contact=contact,
        user_id = user_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)  # ensures the object has an id
    return new_item


def get_item(db: Session, item_id: str):
    return db.query(Item).filter(Item.id == item_id).first()

def delete_item(db: Session, item_id: str):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

def get_item_by_id(db: Session, id: str):
    return db.query(Item).filter(Item.id == id).first()


def create_user(db: Session, username: str, email: str, first_name: str, last_name: str, password: str, is_active: bool = True, is_superuser: bool = False, is_verified: bool = False):
    from .models import User

    new_user = User(
        username=username,
        email=email,
        first_name = first_name,
        last_name = last_name,
        hashed_password=password,  # In a real app, hash the password
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_finder(db: Session, contact: str):
    new_finder = Finder(
        contact=contact
    )
    db.add(new_finder)
    db.commit()
    db.refresh(new_finder)
    return new_finder

def create_finder_if_not_exists(db: Session, contact: str):
    finder = db.query(Finder).filter(Finder.contact == contact).first()
    if not finder:
        finder = create_finder(db, contact)
    return finder



def start_conversation(db: Session, item_id: str, finder_contact: str, owner_email: str, message: str):
    from .models import Conversation, Message, User

    finder = create_finder_if_not_exists(db, finder_contact)
    owner = db.query(User).filter(User.email == owner_email).first()

    if not owner or not finder:
        raise ValueError("Owner or finder not found")

    # Create conversation
    new_conversation = Conversation(
        finder=finder,
        owner_id=owner.id
    )
    new_conversation.participants.append(owner)

    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    # Create initial message
    initial_message = Message(
        conversation_id=new_conversation.id,
        sender_id=owner.id,
        finder_id=finder.id,
        message_content=message,
    )
    db.add(initial_message)
    db.commit()
    db.refresh(initial_message)

    return new_conversation




def get_conversation(db: Session, conversation_id: str):
    from .models import Conversation
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def get_user_conversations(db: Session, user_id: str):
    from .models import Conversation, User
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user.conversations
    return []

def send_message(db: Session, conversation_id: str, sender_id: str, content: str):
    from .models import Message

    new_message = Message(
        content=content,
        sender_id=sender_id,
        conversation_id=conversation_id
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def get_messages(db: Session, conversation_id: str):
    from .models import Message
    return db.query(Message).filter(Message.conversation_id == conversation_id).all()