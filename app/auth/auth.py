from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    create_access_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.database import UserDB
from app.dependencies import get_db
from app.models import User
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Gets the current user based on the provided token.

    Args:
        token (str, optional): The authentication token. Defaults to Depends(oauth2_scheme).
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserDB: The current user retrieved from the database.
    Raises:
        HTTPException: If credentials cannot be validated.
    """

    username = decode_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def register_user(user: User, db: Session = Depends(get_db)):
    """
    Registers a new user in the system.

    Args:
        user (User): The user data to register.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserDB: The newly created user in the database.

    Raises:
        HTTPException: If the username is already registered.
    """

    user_service = UserService(db)
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(user.username, user.password)


def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Logs in a user to generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): The form data containing username and password.
        Defaults to Depends().
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the username or password is incorrect.
    """

    user_service = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
