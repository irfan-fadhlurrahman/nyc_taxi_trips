#!/usr/bin/bash

# Taxi Zones
docker run -it --env-file=.env --network=postgres_pgadmin_default \
taxi_ingest:v002 \
--datetime_columns None \
--url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv \
--table_name taxi_zones \
--chunksize None 


# Yellow Taxi Trips 2021-01
docker run -it --env-file=.env --network=postgres_pgadmin_default \
taxi_ingest:v002 \
--datetime_columns tpep_pickup_datetime tpep_dropoff_datetime \
--url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz \
--table_name taxi_zones \
--chunksize 100000