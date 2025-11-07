from datetime import datetime, timedelta
import io
import uuid
import asyncio
from typing import Optional
import json

from fastapi import FastAPI, Depends, HTTPException, Response, Cookie, Request, Form, APIRouter
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import jwt
from passlib.context import CryptContext
import qrcode
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import SessionLocal, engine, Base
from . import crud, models
from .schemas import ItemCreate, UserCreate, LoginRequest, Settings, ItemPublic, ConversationCreate, MessageCreate
from .email_utils import send_anonymous_email  # your email helper

# ------------------------
# SETTINGS AND INIT
# ------------------------
settings = Settings()  # Load settings from .env file

# Create tables
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# FastAPI app
app = FastAPI()

# Public router
router = APIRouter(prefix="/api/pub", tags=["public"])

# Mount static frontend assets
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ------------------------
# DEPENDENCIES
# ------------------------
def get_db():
    """Yield a database session and close after use"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(access_token: str | None = Cookie(default=None)):
    """Dependency to get currently logged-in user from JWT cookie"""
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return {"user_id": payload["user_id"], "username": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create JWT access token.
    data should include 'sub' (username) and 'user_id'.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ------------------------
# ITEM ENDPOINTS
# ------------------------
class ContactRequest(BaseModel):
    message: str
    finder_contact: str

# --- Public item endpoints ---
@router.post("/item/{id}/contact")
async def contact_item_owner(
    id: str,
    payload: ContactRequest,  # 👈 Now FastAPI expects JSON
    db: Session = Depends(get_db)
):
    item = crud.get_item_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    owner_email = item.owner.email

    print(f"Contact request for item {id}: {payload.message} from {payload.finder_contact} {owner_email}")

    crud.start_conversation(db, item.id, payload.finder_contact, owner_email, payload.message)

    
    #raise Exception("Simulated error for testing")
    return {"status": "Email sent"}


@app.get("/api/pub/item/{item_id}")
def get_public_item(item_id: str, db: Session = Depends(get_db)):
    """Get public item details for frontend display"""
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/pub/getitem/{item_id}")
def get_item_public_endpoint(item_id: str, db: Session = Depends(get_db)):
    """Serve public item HTML page"""
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return FileResponse("frontend/pubitems.html")


@app.get("/qrcode/public/{id}")
def generate_qr_code(id: str, request: Request, db: Session = Depends(get_db)):
    """Generate QR code that links to public item page"""
    item = crud.get_item_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    base_url = str(request.base_url).rstrip("/")
    qr.add_data(f"{base_url}/pub/getitem/{item.id}")
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


# --- Private item endpoints ---
@app.post("/additem", response_model=ItemPublic)
def create_item_endpoint(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add a new item for the logged-in user"""
    return crud.create_item(
        db=db,
        item_description=item.item_description,
        directions=item.directions,
        dropoff_location=item.dropoff_location,
        contact=item.contact,
        user_id=current_user["user_id"]
    )

@app.get("/remove/{item_id}")
def remove_item_endpoint(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Remove an item owned by the logged-in user"""
    item = crud.get_item(db, item_id)
    if not item or item.user_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")
    
    crud.delete_item(db, item_id)
    return FileResponse("frontend/youritems.html")

@app.get("/priv/getitems")
def get_user_items(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all items belonging to logged-in user"""
    items = db.query(models.Item).filter(models.Item.user_id == current_user["user_id"]).all()
    return items


@app.get("/priv/getitem/{item_id}")
def get_item_private_endpoint(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Serve private item page for the owner"""
    item = crud.get_item(db, item_id)
    if not item or item.user_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Item not found")
    return FileResponse("frontend/item.html")


@app.get("/api/priv/item/{item_id}", response_model=ItemPublic)
def get_item_data(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """API endpoint for frontend JS to fetch private item data"""
    item = crud.get_item(db, item_id)
    if not item or item.user_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/api/priv/item/{item_id}", response_model=ItemPublic)
def update_item_data(
    item_id: str,
    item_update: ItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update an existing item"""
    item = crud.get_item(db, item_id)
    if not item or item.user_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.item_description = item_update.item_description
    item.directions = item_update.directions
    item.dropoff_location = item_update.dropoff_location
    item.contact = item_update.contact
    db.commit()
    db.refresh(item)
    return item


# Serve frontend pages
@app.get("/additem")
def server_additem_page():
    return FileResponse("frontend/additem.html")


@app.get("/youritems")
def serve_youritems_page():
    return FileResponse("frontend/youritems.html")


# Include public router
app.include_router(router)


# ------------------------
# AUTHENTICATION ENDPOINTS
# ------------------------
@app.post("/login")
def login_user(login: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """Authenticate user and set JWT token cookie"""
    if "@" in login.username:
        user = db.query(models.User).filter(models.User.email == login.username).first()
    else:
       user = db.query(models.User).filter(models.User.username == login.username).first()


    if not user or not pwd_context.verify(login.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"message": "Login successful"}


@app.post("/logout")
def logout_user(response: Response):
    """Logout user by deleting JWT cookie"""
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register new user with validations"""
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if user.email != user.email_confirm:
        raise HTTPException(status_code=400, detail="Emails do not match")
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
        first_name=user.first_name,
        last_name=user.last_name,
        password=pwd_context.hash(user.password)
    )


# ------------------------
# USER PROFILE ENDPOINTS
# ------------------------
@app.get("/userinfo")
def profile(current_user: dict = Depends(get_current_user)):
    """Return current user info"""
    return {"user_id": current_user["user_id"], "username": current_user["username"]}


@app.get("/profile")
def serve_profile():
    """Serve profile HTML page"""
    return FileResponse("frontend/profile.html")

@app.get("/settings")
def serve_profile():
    """Serve profile HTML page"""
    return FileResponse("frontend/settings.html")


# ------------------------
# HOME PAGE
# ------------------------
@app.get("/")
def home_page():
    return FileResponse("frontend/landing.html")


@app.get("/register")
def serve_register():
    return FileResponse("frontend/register.html")


@app.get("/login")
def serve_register():
    return FileResponse("frontend/login.html")


#------------------------
# CHAT
#------------------------

def get_current_user_optional(access_token: str | None = Cookie(default=None)):
    if not access_token:
        return None  # <-- allow finders
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return {"user_id": payload["user_id"], "username": payload["sub"]}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None

@app.get("/pub/chat/{conversation_id}")
async def get_conversation_page(
    conversation_id: str,
    guest: str | None = None,
    db: Session = Depends(get_db),
    current_user: dict | None = Depends(get_current_user_optional)
):
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    allowed = False
    if current_user:
        if conversation.owner_id == current_user["user_id"]:
            allowed = True
        # elif conversation.finder_user_id == current_user["user_id"]:
        #     allowed = True
    elif guest:
        if conversation.finder_id == guest:
            allowed = True

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized to access this conversation")

    return FileResponse("frontend/chatpub.html")




@app.get("/pub/chat/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: str, db: Session = Depends(get_db)):
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation.messages



@app.post("/pub/chat/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    message_data: MessageCreate,  # schema with field: content: str
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_optional),  # optional
    request: Request = None
):
    # 1️⃣ Find the conversation
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 2️⃣ Determine sender type
    sender_id = None
    finder_id = None

    if current_user:
        # Logged-in user
       sender_id = current_user["user_id"]
    else:
        # Anonymous finder — you could store finder_id in cookies/session
        finder = conversation.finder
        if finder:
            finder_id = finder.id

    # 3️⃣ Create and save message
    new_message = models.Message(
        conversation_id=conversation.id,
        sender_id=sender_id,
        finder_id=finder_id,
        message_content=message_data.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


def start_finder_conversation(db, item_id, finder_email, owner_email, message):
    finder_id = str(uuid.uuid4())  # unique, hard to guess
    finder = crud.create_finder(db, finder_id=finder_id, email=finder_email)
    conversation = crud.create_conversation(
        db,
        item_id=item_id,
        finder_user_id=None,  # finder, not signed-in
        finder_id=finder.id,
        owner_email=owner_email,
        initial_message=message
    )
    return conversation, finder_id



@app.post("/api/pub/item/{item_id}/start_chat")
async def start_conversation_endpoint(
    item_id: str,
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db)
):
    item = crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    owner_email = item.owner.email

    conversation = crud.start_conversation(
        db,
        item.id,
        conversation_data.finder_contact,
        owner_email,
        conversation_data.message
    )
    return {"conversation_id": conversation.id}


@app.get("/pub/chat/{conversation_id}/stream")
async def message_stream(
    conversation_id: str,
    request: Request,
    guest: str | None = None,  # guest_id from query string
    db: Session = Depends(get_db),
    current_user: dict | None = Depends(get_current_user_optional),  # optional for logged-in users
):
    """
    SSE endpoint to stream messages for both logged-in users and guests.
    Guests are verified using the `guest` query parameter.
    """
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 1️⃣ Verify access
    allowed = False
    if current_user:
        # Logged-in user: owner or finder
        if conversation.owner_id == current_user["user_id"]:
            allowed = True
        elif getattr(conversation.finder_user, "id", None) == current_user["user_id"]:
            allowed = True
    elif guest:
        # Guest: check guest_id matches
        if conversation.finder_id == guest:
            allowed = True

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized to access this conversation")

    async def event_generator():
        # Start from the first message timestamp to get the chat history
        last_timestamp = conversation.messages[0].timestamp if conversation.messages else datetime.min

        while True:
            if await request.is_disconnected():
                break

            new_messages = db.query(models.Message).filter(
                models.Message.conversation_id == conversation_id,
                models.Message.timestamp > last_timestamp
            ).order_by(models.Message.timestamp.asc()).all()

            for msg in new_messages:
                sent_by_current_user = False
                if current_user and msg.sender_id == current_user.get("user_id"):
                    sent_by_current_user = True
                elif not current_user and guest and msg.finder_id == guest:
                    sent_by_current_user = True

                display_name = "You" if sent_by_current_user else ("Owner" if msg.sender_id else "Finder")
                message_data = {
                    "id": msg.id,
                    "content": msg.message_content,
                    "timestamp": msg.timestamp.strftime("%I:%M %p"),
                    "sender_type": "you" if sent_by_current_user else ("owner" if msg.sender_id else "finder"),
                    "sender_name": display_name
                }
                yield f"data: {json.dumps(message_data)}\n\n"

            # Update last_timestamp after all messages are processed
            if new_messages:
                last_timestamp = new_messages[-1].timestamp

            await asyncio.sleep(1)


    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.get("/mychats")
def serve_mychats_page():
    """Serve the user's chats page"""
    return FileResponse("frontend/mychats.html")

@app.get("/api/priv/mychats")
def get_user_conversations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all conversations for the logged-in user"""
    conversations = crud.get_user_conversations(db, current_user["user_id"])
    return conversations


