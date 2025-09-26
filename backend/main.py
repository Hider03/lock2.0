from datetime import datetime, timedelta
import io
from fastapi import FastAPI, Depends, HTTPException, Response  # ✅ Response comes from fastapi

import uuid
from fastapi import Cookie, FastAPI, Depends, HTTPException, Response
import jwt
from passlib.context import CryptContext
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import qrcode
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from .database import SessionLocal, engine, Base
from . import crud, models
from .schemas import ItemCreate, UserCreate, LoginRequest


# Create secret key for JWT choose algorithm and token expiration time
SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Create tables
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# JWT helper creates the access token for the user
# data should include "sub" (subject, usually username) and "user_id"
# expires_delta is optional timedelta for expiration
# This functions works by copying the data, adding an expiration time, and encoding it with the secret key
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get current user
# access_token is read from HttpOnly cookie
def get_current_user(access_token: str | None = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user_id": payload["user_id"], "username": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    

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

# Home page 
@app.get("/")
def home_page():
    return FileResponse("frontend/landing.html")


@app.get("/register")
def serve_register():
    return FileResponse("frontend/register.html")

@app.get("/login")
def serve_login():
    return FileResponse("frontend/login.html")


# This works by verifying the username and password, creating a JWT token, and setting it in an HttpOnly cookie
@app.post("/login")
def login_user(login: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == login.username).first()
    if not user or not pwd_context.verify(login.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {"message": "Login successful"}


# Logout endpoint
# This works by deleting the cookie by doing response.delete_cookie which sets max_age=0 it knows that it is the users by the key name which is "access_token" 
@app.post("/logout")
# response in this case is from fastapi import Response which is explained as a class for creating HTTP responses
def logout_user(response: Response):
    # Delete the cookie by setting max_age=0
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}


# Protected profile endpoint
# This is used in javascript fetch to get the user info after login by doing a GET request to /profile with the cookie automatically included
@app.get("/userinfo")
def profile(current_user: dict = Depends(get_current_user)):
    # You have access to the logged-in user's info
    return {"user_id": current_user["user_id"], "username": current_user["username"]}

@app.get("/profile")
def serve_profile():
    return FileResponse("frontend/profile.html")



# POST endpoint
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if db.query(models.User).filter(models.User.email == user.email).first():
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
