from sqlalchemy.orm import Session
from app.models import Package, Report
from app.database import PackageDB
from datetime import date
import logging

logger = logging.getLogger(__name__)


class CargoService:
    """
    A service class for managing cargo-related operations.

    Handles adding a package to the database and generating a report based on packages for a specific date.
    """

    def __init__(self, db: Session):
        self.db = db

    def add_package(self, package: Package):
        db_package = PackageDB(**package.dict())
        self.db.add(db_package)
        self.db.commit()
        self.db.refresh(db_package)
        logger.info(f"Package added: {db_package.id}")
        return db_package

    def generate_report(self, report_date: date) -> Report:
        packages_on_date = self.db.query(PackageDB).filter(PackageDB.date == report_date).all()
        total_packages = len(packages_on_date)
        total_revenue = total_packages * 10
        logger.info(f"Report generated for date {report_date}: {total_packages} packages, {total_revenue} revenue")
        return Report(total_packages=total_packages, total_revenue=total_revenue)
