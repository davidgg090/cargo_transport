from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PackageDB(Base):
    """
    A class representing a package in the database.

    Represents a package with attributes such as client, weight, origin, destination, and date.
    """

    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    client = Column(String, index=True)
    weight = Column(Float)
    origin = Column(String)
    destination = Column(String)
    date = Column(Date)


class UserDB(Base):
    """
    A class representing a user in the database.

    Represents a user with attributes such as username and hashed_password.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


Base.metadata.create_all(bind=engine)
