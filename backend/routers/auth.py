# Import this at top after creating auth.py
from auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from auth import authenticate_user, create_access_token, EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login with username and password.
    Returns JWT token to use in all other API calls.
    """
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Incorrect username or password",
            headers     = {"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data            = {"sub": user["username"]},
        expires_delta   = timedelta(minutes=EXPIRE_MINUTES)
    )
    
    return {
        "access_token"  : access_token,
        "token_type"    : "bearer",
        "username"      : user["username"],
        "expires_in"    : f"{EXPIRE_MINUTES} minutes"
    }


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Get current logged in user info"""
    return {
        "username"  : current_user["username"],
        "full_name" : current_user["full_name"],
        "is_active" : current_user["is_active"]
    }


