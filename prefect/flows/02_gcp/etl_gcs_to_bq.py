import pandas as pd

from pathlib import Path

from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download data from Cloud Storage"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoomcamp-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path="data/")
    
    return Path(f"data/{gcs_path}")

@task(log_prints=True)
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    
    # Check missing values in some columns
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df['passenger_count'].fillna(0)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")    
    
    return df

@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("gcp-credentials")
    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="dtc-de-course-375301",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists='append'
    )

@flow()
def etl_gcs_to_bq() -> None:
    """Main ETL flow to load data into BigQuery"""
    color = "yellow"
    year = 2021
    month = 1
    
    # Task starts here
    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)
    
if __name__ == "__main__":
    etl_gcs_to_bq()