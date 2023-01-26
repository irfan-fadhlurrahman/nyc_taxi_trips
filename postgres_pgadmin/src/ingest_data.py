import os
import time
import logging
import argparse

import pandas as pd
import db_credentials as dbc

from pathlib import Path

# Define logging
logging.basicConfig(
    filename='ingestion.log',
    filemode='a',
    format=f'%(asctime)s - {__file__} %(message)s', 
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S'
)

class NYCGovTaxiToPostgresPipeline:
    
    def __init__(self, datetime_columns: list):
        self.engine = dbc.PostgresConnection(db_conn=dbc.get_database_credentials()).engine()
        self.datetime_columns = datetime_columns
        self.engine.connect()
    
    def extract(self, url: str, chunksize: int) -> pd.DataFrame:
        """Return the dataframe of downloaded file"""
        # Rename the downloaded file
        if url.endswith('.csv.gz'):
            csv_name = 'output.csv.gz'
        else:
            csv_name = 'output.csv'
        
        # Define file path then download it
        os.system('mkdir dataset')
        path = Path(f"dataset/{csv_name}")
        if not os.path.exists(path):
            os.system(f"wget {url} -O {path}")
        
        # To avoid error if chunksize is not integer
        if isinstance(chunksize, int):
            return pd.read_csv(path, iterator=True, chunksize=chunksize)
        else:
            return pd.read_csv(path, iterator=True)
        
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return the cleaned dataframe"""
        # Change dtype of selected columns
        if self.datetime_columns:
            for col in self.datetime_columns:
                if col in df.columns.tolist():
                    df[col] = pd.to_datetime(df[col])
        
        # Make column names uniform
        df.columns = df.columns.str.lower()
        
        return df

    def load(self, df: pd.DataFrame, table_name: str, if_exists: str) -> None:
        """Ingest each chunks of cleaned dataframe to postgres database"""
        self.transform(df).to_sql(
            name=table_name, 
            con=self.engine, 
            if_exists=if_exists
        )
        
def run(params):
    # Input
    datetime_columns = params.datetime_columns
    url = params.url
    table_name = params.table_name
    try:
        chunksize = int(params.chunksize)
    except:
        chunksize = params.chunksize
    
    # Define pipeline class
    pipeline = NYCGovTaxiToPostgresPipeline(datetime_columns)
    
    # Create a table on the database
    header = next(pipeline.extract(url, chunksize=chunksize)).head(n=0)
    pipeline.load(header, table_name, if_exists='replace')
    
    logging.info(f"Extracting the data from {url}")
    
    # Load data into a created table
    for df in pipeline.extract(url, chunksize=chunksize):
        start = time.time()
        pipeline.load(df, table_name, if_exists='append')
        end = time.time()
        
        logging.info(f"Ingestion of {len(df)} rows to table {table_name} took {end-start:.2f} seconds")
    
    logging.info(f"Ingestion to table {table_name} finished")
    
if __name__ == "__main__":
    # Initialize
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # Args
    parser.add_argument(
        '--datetime_columns', 
        nargs="+", 
        default=["tpep_pickup_datetime", "tpep_dropoff_datetime"], 
        required=True, 
        help='time columns to be changed their dtypes'
    )
    parser.add_argument(
        '--url', 
        required=True, 
        help='url of the csv file'
    )
    parser.add_argument(
        '--table_name', 
        required=True, 
        help='name of the table where we will write the results to'
    )
    parser.add_argument(
        '--chunksize', 
        required=True, 
        help='number of rows of dataframe to be ingested per batch'
    )
    
    # Run
    args = parser.parse_args()
    run(args)
    
        
        