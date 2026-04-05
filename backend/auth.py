from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY      = os.getenv("SECRET_KEY")
ALGORITHM       = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINUTES  = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

pwd_context     = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme   = OAuth2PasswordBearer(tokenUrl="auth/login")

# =============================================
# Hardcoded users for now (Week 1 simple auth)
# Later we'll move this to DB
# =============================================
USERS_DB = {
    "admin": {
        "username"          : "admin",
        "hashed_password"   : pwd_context.hash("admin123"),  # Change this!
        "full_name"         : "Admin User",
        "is_active"         : True
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = USERS_DB.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta 
        else timedelta(minutes=EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail      = "Invalid or expired token",
        headers     = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload     = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username    = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = USERS_DB.get(username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
        