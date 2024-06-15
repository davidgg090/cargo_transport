from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates an access token based on the provided data.

    Args:
        data (dict): The data to be encoded into the token.
        expires_delta (Optional[timedelta], optional): The expiration time delta. Defaults to None.

    Returns:
        str: The encoded JWT access token.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    """
    Verifies if a plain password matches a hashed password.

    Args:
        plain_password: The plain password to be verified.
        hashed_password: The hashed password for comparison.

    Returns:
        bool: True if the passwords match, False otherwise.
    """

    return plain_password == hashed_password


def get_password_hash(password):
    """
    Returns the hashed version of a password.

    Args:
        password: The password to be hashed.

    Returns:
        str: The hashed password.
    """

    return password


def decode_token(token: str):
    """
    Decodes a JWT token to extract the username.

    Args:
        token (str): The JWT token to decode.

    Returns:
        str: The username extracted from the token, or None if decoding fails.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError as e:
        logger.error(f"Token decoding error: {str(e)}")
        return None
