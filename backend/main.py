import io
import uuid
from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import qrcode
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from .database import SessionLocal, engine, Base
from . import crud
from schemas import ItemCreate, UserCreate

# Create tables
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
@app.get("/finder/")
def serve_index():
    return FileResponse("frontend/index.html")

# Home page 
@app.get("/")
def home_page():
    return FileResponse("frontend/landing.html")


# POST endpoint
@app.post("/register/")
def create_item_endpoint(user: UserCreate, db: Session = Depends(get_db)):

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if db.query(crud.User).filter(crud.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if db.query(crud.User).filter(crud.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered") 
    
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")  
    

    return crud.create_user(
        db=db,
        username=user.username,
        email=user.email,
        first_name = user.first_name,
        last_name = user.last_name,
        password=pwd_context.hash(user.password)  # Hash the password before storing

    )