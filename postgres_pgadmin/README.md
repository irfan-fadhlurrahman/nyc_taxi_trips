# Host PostgreSQL and pgAdmin on Docker Container

Create a PostgreSQL database with user-interface pgAdmin on Docker.

## Tools
1. Python 3.9
2. PostgreSQL 13
3. pgAdmin 4
4. Docker 

## Setup
Use VSCode to ease the port mapping.

Before creating a virtual environment and run the docker, go to the project directory.
```
cd ~/nyc_taxi_trips/postgres_pgadmin
```

### 1. Virtual Environment
Create:
```
pipenv install --python 3.9 --requirements requirements.txt
```

Activate on project directory:
```
pipenv shell
```

### 2. Configure PostgreSQL and pgAdmin
Start the PostgreSQL and pgAdmin.
```
docker-compose up -d
```

If pgAdmin got an error, stop docker-compose and change the permission then re-run it.
```
sudo chown 5050:5050 data/data_pgadmin
```

Create a server for database
* Click Register -> Server
[img]()
* Define the server name
[img]()
* Define hostname, username, and password as per [docker-compose.yaml]() then click save
[img]()

### 3. Ingest the dataset into Postgres database
Build docker image for [ingest_data.py]()
```
docker build -t taxi_ingest:v001 .
```

Find the network of docker-compose.
```
docker network ls
```
In my case, it is **postgres_pgadmin_default**.

Run the container.
```
docker run -it \
   --network=postgres_pgadmin_default \
    taxi_ingest:v001 \
   --user=root \
   --password=root \
   --host=pgdatabase \
   --port=5432 \
   --db=ny_taxi \
   --table_name=yellow_taxi_trips \
   --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```