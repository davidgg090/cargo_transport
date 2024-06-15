from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handles HTTP exceptions by logging the error and returning a JSON response.

    Args:
        request (Request): The request object.
        exc (HTTPException): The HTTP exception to handle.

    Returns:
        JSONResponse: A JSON response with the error message.
    """

    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
