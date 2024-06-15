from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.models import PackageCreate, PackageResponse, Report
from app.services.cargo_service import CargoService
from app.dependencies import get_db
from app.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/packages/", response_model=PackageResponse)
def add_package(package: PackageCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """
    Adds a new package to the system.

    Args:
        package (PackageCreate): The package data to add.

    Returns:
        PackageResponse: The response containing the added package details.

    Raises:
        HTTPException: If there is an error adding the package.
    """

    cargo_service = CargoService(db)
    try:
        return cargo_service.add_package(package)
    except Exception as e:
        logger.error(f"Error adding package: {str(e)}")
        raise HTTPException(status_code=500, detail="Error adding package")


@router.get("/report/", response_model=Report)
def get_report(report_date: date, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """
    Retrieves a report based on the specified date.

    Args:
        report_date (date): The date for which the report is generated.

    Returns:
        Report: The generated report.

    Raises:
        HTTPException: If there is an error generating the report.
    """

    cargo_service = CargoService(db)
    try:
        return cargo_service.generate_report(report_date)
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating report")
