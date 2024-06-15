import logging

from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_password_hash, verify_password
from app.database import UserDB

logger = logging.getLogger(__name__)


class UserService:
    """
    A service class for managing user-related operations.

    Handles creating a new user in the database and authenticating users based on provided credentials.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, password: str):
        hashed_password = get_password_hash(password)
        db_user = UserDB(username=username, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"User created: {username}")
        return db_user

    def authenticate_user(self, username: str, password: str):
        user = self.db.query(UserDB).filter(UserDB.username == username).first()
        if user and verify_password(password, user.hashed_password):
            logger.info(f"User authenticated: {username}")
            return user
        logger.warning(f"Failed authentication attempt for user: {username}")
        return None
