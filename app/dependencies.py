from app.database import SessionLocal
from sqlalchemy.orm import Session


def get_db():
    """
    Returns a generator that provides a database session.

    Yields a database session that needs to be closed after use.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
