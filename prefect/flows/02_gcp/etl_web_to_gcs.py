import pandas as pd

from pathlib import Path

from prefect import task, flow
from prefect_gcp.cloud_storage import GcsBucket

# from random import randint

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into Pandas DataFrame"""
    
    # crete an error to try a retry
    # if randint(0, 1) > 0:
    #     raise Exception
    
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {df.shape}")
    
    return df

@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as Parquet file"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    
    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to gcs"""
    gcs_block = GcsBucket.load("zoomcamp-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)

@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    # Input variables
    color = "yellow"
    year = 2021
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    # Task starts here
    df = fetch(dataset_url)
    df = clean(df)
    
    # Task to upload the parquet file to Cloud Storage
    path = write_local(df, color, dataset_file)
    write_gcs(path)

if __name__ == "__main__":
    etl_web_to_gcs()