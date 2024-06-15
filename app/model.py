from pydantic import BaseModel
from datetime import date
from typing import Optional


class Package(BaseModel):
    """
    A data model class representing a package.

    Represents a package with attributes such as id, client, weight, origin, destination, and date.
    """

    id: int
    client: str
    weight: float
    origin: str
    destination: str
    date: date


class Report(BaseModel):
    """
    A data model class representing a report.

    Represents a report with attributes such as total_packages and total_revenue.
    """

    total_packages: int
    total_revenue: float


class User(BaseModel):
    """
    A data model class representing a user.

    Represents a user with attributes such as username and password.
    """

    username: str
    password: str


class Token(BaseModel):
    """
    A data model class representing a token.

    Represents a token with attributes such as access_token and token_type.
    """

    access_token: str
    token_type: str
