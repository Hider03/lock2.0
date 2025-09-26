from fastapi import FastAPI, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

# JWT helper
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get current user
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

# Login endpoint
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
        secure=False,       # True in production with HTTPS
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {"message": "Login successful"}

# Protected profile endpoint
@app.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    # You have access to the logged-in user's info
    return {"user_id": current_user["user_id"], "username": current_user["username"]}

# Logout endpoint
@app.post("/logout")
def logout_user(response: Response):
    # Delete the cookie by setting max_age=0
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}
