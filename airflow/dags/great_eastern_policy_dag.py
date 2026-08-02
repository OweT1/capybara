"""
Airflow DAG for policy extraction for Great Eastern.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from airflow.sdk import dag, task

default_args = {
    "owner": "data_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


# 2. Instantiate the DAG using the @dag decorator
@dag(
    dag_id="great_eastern_files_download",
    default_args=default_args,
    description="An ETL Pipeline to scrap and download policy PDF files from Great Eastern",
    schedule="@daily",  # Runs once a day at midnight
    start_date=datetime(2026, 1, 1),  # Start tracking execution from this date
    catchup=False,  # Prevents backfilling missed historical runs
    tags=["production", "etl"],
)
def great_eastern_etl_workflow():
    from src.policies.great_eastern import (
        extract_links as _extract_links,
        extract_files as _extract_files,
    )

    @task
    def extract_links():
        _extract_links()

    @task
    def extract_files():
        _extract_files()

    extract_links()
    extract_files()


great_eastern_etl_workflow()
