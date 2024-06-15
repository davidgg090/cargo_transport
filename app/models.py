from datetime import date

from pydantic import BaseModel


class PackageBase(BaseModel):
    """
    A base data model class representing the attributes of a package.

    Represents a package with attributes such as client, weight, origin, destination, and date.
    """

    client: str
    weight: float
    origin: str
    destination: str
    date: date


class PackageCreate(PackageBase):
    """
    A data model class for creating a package.

    Inherits attributes from PackageBase for creating a new package.
    """

    pass


class PackageResponse(PackageBase):
    """
    A data model class for a package response.

    Inherits attributes from PackageBase and includes an additional id attribute.
    """

    id: int

    class Config:
        from_attributes = True


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


class UserResponse(BaseModel):
    """
    A data model class for a user response.

    Includes the username attribute and uses from_attributes configuration.
    """

    username: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """
    A data model class representing a token.

    Represents a token with attributes such as access_token and token_type.
    """

    access_token: str
    token_type: str
