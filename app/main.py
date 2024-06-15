import logging

from fastapi import FastAPI, Depends, HTTPException

from app.auth.auth import get_current_user
from app.exceptions import http_exception_handler
from app.routers import cargo, auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)


app.include_router(cargo.router, prefix="/cargo", tags=["cargo"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/secure-endpoint/")
def read_secure_data(user: str = Depends(get_current_user)):
    """
    Reads secure data for an authenticated user.

    Args:
        user (str): The authenticated user.

    Returns:
        dict: A message confirming authentication along with the user information.
    """

    return {"message": "You are authenticated", "user": user}
