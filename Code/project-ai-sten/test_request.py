import influxdb_client
import os
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client_3 import InfluxDBClient3


URL_INFLUDB = "http://localhost:8086"
ORG = "AP"
TOKEN = "m2prwh_b-sKjBD_JBT36OM4NPf4LzWHfzEX2_LDHv2osBImuSIikJsH2mX9YV3_uluQLVzxBW4qncD_ZdEozMg=="
BUCKET = "BE-OpenAQ-sensors"

DBclient = influxdb_client.InfluxDBClient(
    url=URL_INFLUDB, token=TOKEN, org=ORG)
read_api = DBclient.query_api()


query = f'from(bucket: "{BUCKET}")\
            |> range(start: 0)\
            |> filter(fn: (r) => r["_measurement"] == "sensor")\
 			|> filter(fn: (r) => r["_field"] == "lat" or r["_field"] == "lon")\
 			|> last()'

results = read_api.query(org=ORG, query=query)
for result in results:
    print(result.records)
