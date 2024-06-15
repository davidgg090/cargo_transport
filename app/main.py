from fastapi import FastAPI, Depends, HTTPException
from app.routers import cargo, auth
from app.exceptions import http_exception_handler
from app.auth.auth import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cargo Transport API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(cargo.router, prefix="/cargo", tags=["cargo"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/secure-endpoint/")
def read_secure_data(user: str = Depends(get_current_user)):
    return {"message": "You are authenticated", "user": user}


app.add_exception_handler(HTTPException, http_exception_handler)
