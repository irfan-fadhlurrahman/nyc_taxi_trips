import os

from dataclasses import dataclass
from dotenv import load_dotenv
from sqlalchemy import create_engine

@dataclass
class DBConnection:
    user: str
    password: str
    host: str
    port: int
    table_name: str
    
class PostgresConnection:
    def __init__(self, db_conn: DBConnection):
        self.connection_url = f"postgresql+psycopg2://{db_conn.user}:{db_conn.password}@{db_conn.host}:{db_conn.port}/{db_conn.table_name}"
    
    def engine(self):
        return create_engine(self.connection_url)

def get_database_credentials() -> DBConnection:
    # Load environment variables from other directory
    load_dotenv()
        
    return DBConnection(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=int(os.environ.get("POSTGRES_PORT")),
        table_name=os.environ.get("POSTGRES_DB")
    )

def main():
    engine = PostgresConnection(db_conn=get_database_credentials()).engine()
    print(engine.connect())


if __name__ == "__main__":
    main()