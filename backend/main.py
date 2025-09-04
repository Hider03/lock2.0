import io
import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import qrcode
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from .database import SessionLocal, engine, Base
from . import crud

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount the frontend folder for CSS/JS
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema
class ItemCreate(BaseModel):
    item_description: str
    directions: str
    dropoff_location: str
    contact: Optional[str] = None  # optional

# POST endpoint
@app.post("/items/")
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(
        db=db,
        item_description=item.item_description,
        directions=item.directions,
        dropoff_location=item.dropoff_location,
        contact=item.contact
    )

@app.get("/items/{item_id}")
def serve_item_page(item_id: str):
    return FileResponse("frontend/item.html")




@app.get("/api/items/{item_id}")
def get_item(item_id: str, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Serve the main HTML file
@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")
