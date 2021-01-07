# Install Hive with docker-compose

## Push source code
git clone https://github.com/big-data-europe/docker-hive.git

## Start docker-compose
sudo docker-compose up -d

## SSH to container
sudo docker exec -it docker-hive_hive-server_1 /bin/bash

# Hive with docker-compose

## Use hive2

/opt/hive/bin/beeline -u jdbc:hive2://localhost:10000

## Show DB

show databases;

## Run Hive script 
hive -f SEMX_MCD-KOL_MST_CUSTOMER.sql

## Create TB with ksdev_semX_mcd

hive -e "Drop TABLE IF EXISTS KOL_MST_CUSTOMER";

## Show detial of table
describe kol_mst_customer;

## Delete table
hive -e "Drop TABLE IF EXISTS KOL_MST_CUSTOMER";