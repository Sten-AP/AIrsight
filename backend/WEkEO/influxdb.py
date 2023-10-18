from influxdb_client_3 import InfluxDBClient3
import pandas as pd
import time
import netCDF4 as nc
import os

URL_INFLUDB = "http://localhost:8086"
ORG = "AP"
TOKEN = "wDRpb-ELk-yHqG98wB0bUr7B84aqnlYPeV8EsfV2ROOjTiWS12MWlPI7Ty39Cbvmq504f249srd--yKwlLVyIw=="
BUCKET = "WEkEO"

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"./data"
NOW = pd.Timestamp.now(tz='UCT').floor('ms')

client = InfluxDBClient3(host=URL_INFLUDB, token=TOKEN,
                         org=ORG, database=BUCKET, enable_gzip=True)

nc_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.nc')]

# print(data_file.__dict__)  

# data = {}
# for data in data_file.dimensions.values():
#     print(data)

data_dict = {}
for nc_file in nc_files:
    file = nc.Dataset(DATA_DIR + "/" + nc_file)
    for data in file.dimensions.values():
        print(data)