from app.database import SessionLocal


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
