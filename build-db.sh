#!/bin/bash

SCHEMA=public
TABLE_NAME=zip_code
DB_NAME=gistest

if [[ -z "tl_2014_us_zcta510.zip" ]]; then
  curl ftp://ftp2.census.gov/geo/tiger/TIGER2014/ZCTA5/tl_2014_us_zcta510.zip
fi

mkdir zcta510
unzip tl_2014_us_zcta510.zip -d zcta510

rm tl_2014_us_zcta510.zip
cd zcta510

shp2pgsql -s 4326 tl_2014_us_zcta510 ${SCHEMA}.${TABLE_NAME} > load_${TABLE_NAME}.sql

psql -d ${DB_NAME} -f load_${TABLE_NAME}.sql
