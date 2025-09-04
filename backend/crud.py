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
