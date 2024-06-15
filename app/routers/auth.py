from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.models import User, UserResponse, Token
from app.auth.auth import register_user, login_for_access_token
from app.dependencies import get_db

router = APIRouter()


@router.post("/register/", response_model=UserResponse)
def register(user: User, db: Session = Depends(get_db)):
    """
    Registers a new user in the system.

    Args:
        user (User): The user data to register.

    Returns:
        dict: A dictionary containing the username of the newly registered user.
    """

    new_user = register_user(user, db)
    return {"username": new_user.username}


@router.post("/token/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Logs in a user to generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): The form data containing username and password.

    Returns:
        Token: The generated access token.
    """

    return login_for_access_token(form_data, db)
