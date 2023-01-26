#!/usr/bin/bash

# Change some value of .env variables
export POSTGRES_HOST=localhost

# Activate virtual environment
cd ~/nyc_taxi_trips/postgres_pgadmin; pipenv shell

# Run the script
# Taxi Zones
python ~/nyc_taxi_trips/postgres_pgadmin/src/ingest_data.py \
--datetime_columns None \
--url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv \
--table_name taxi_zones \
--chunksize None 

# Yellow Taxi Trips 2021-01
python ~/nyc_taxi_trips/postgres_pgadmin/src/ingest_data.py \
--datetime_columns tpep_pickup_datetime tpep_dropoff_datetime \
--url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz \
--table_name taxi_zones \
--chunksize 100000 

