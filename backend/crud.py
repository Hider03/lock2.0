from sqlalchemy.orm import Session
from .models import Item
import secrets

def create_item(db: Session, item_description, directions, dropoff_location, contact):
    from .models import Item
    new_item = Item(
        item_description=item_description,
        directions=directions,
        dropoff_location=dropoff_location,
        contact=contact
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)  # ensures the object has an id
    return new_item


def get_item(db: Session, item_id: str):
    return db.query(Item).filter(Item.id == item_id).first()


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