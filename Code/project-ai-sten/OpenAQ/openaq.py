import requests
import json
import pandas as pd
from datetime import datetime
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client_3 import InfluxDBClient3, Point, WritePrecision
import time
import os

URL_INFLUDB = "http://localhost:8086"
ORG = "AP"
TOKEN = "s5ZKgMPFm4EEZigyyL87LvrVF3b0wAwTipKwtQsetKFr3PHsqbWto5hpkwTmGrYCitjbrq5dBS9n_hFF5yUjqA=="
BUCKET = "BE-OpenAQ-sensors"

URL_OPENAQ = "https://api.openaq.org/v2/locations?limit=10000&page=1&offset=0&sort=desc&radius=1000&country_id=134&order_by=lastUpdated&dump_raw=false"
HEADERS = {"accept": "application/json"}
NOW = pd.Timestamp.now(tz='UCT').floor('ms')

response = requests.get(url=URL_OPENAQ, headers=HEADERS)
client = InfluxDBClient3(host=URL_INFLUDB, token=TOKEN,
                         org=ORG, database=BUCKET, enable_gzip=True)

with open('openaq_data.json', 'w') as file:
    file.write(str(response.text))

sensoren = []
for data in response.json()['results']:
    pm10, pm25 = -1, -1
    for parameter in data["parameters"]:
        if parameter['id'] == 1:
            if parameter['lastValue'] != -999:
                pm10 = parameter["lastValue"]
        if parameter['id'] == 2:
            if parameter['lastValue'] != -999:
                pm25 = parameter["lastValue"]

    sensoren.append({
        'name': data['name'],
        'id': data['id'],
        'lat': data['coordinates']['latitude'],
        'lon': data['coordinates']['longitude'],
        'pm10': pm10,
        'pm25': pm25,
        'time': NOW
    })

sensoren_df = pd.DataFrame(sensoren).set_index('time')
print(sensoren_df)

try:
    client.write(sensoren_df, data_frame_measurement_name='sensor',
                 data_frame_tag_columns=['name', 'id'])
except Exception as e:  
    print(f"Error bij point: {e}")
time.sleep(2)
