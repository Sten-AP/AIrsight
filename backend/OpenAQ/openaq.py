import requests
import pandas as pd
#from influxdb_client_3 import InfluxDBClient3
import time
import os

ORG = "AP"
BUCKET = "BE-OpenAQ-sensors"
URL_INFLUDB = "http://localhost:8086"
TOKEN = "g437M2sQpWSzGsMehL7VbTVqMIRvG3xbG4z2iY03f0XBQuhI4m8XCgzPi0I7_i8iNEx1cYnnnta9r7iZbQfnOQ=="

URL_OPENAQ = "https://api.openaq.org/v2/locations?limit=10000&page=1&offset=0&sort=desc&radius=1000&country_id=134&order_by=lastUpdated&dump_raw=false"
HEADERS = {"accept": "application/json"}

NOW = pd.Timestamp.now(tz='UCT').floor('ms')
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"./data"

response = requests.get(url=URL_OPENAQ, headers=HEADERS)
#client = InfluxDBClient3(host=URL_INFLUDB, token=TOKEN, org=ORG, database=BUCKET, enable_gzip=True)


if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

with open(DATA_DIR+'\openaq_data.json', 'w') as file:
    file.write(str(response.text))

sensors = []
for data in response.json()['results']:
    pm10, pm25 = -1, -1
    for parameter in data["parameters"]:
        if parameter['id'] == 1:
            if parameter['lastValue'] != -999:
                pm10 = parameter["lastValue"]
        if parameter['id'] == 2:
            if parameter['lastValue'] != -999:
                pm25 = parameter["lastValue"]

    sensors.append({
        'name': data['name'],
        'id': data['id'],
        'lat': data['coordinates']['latitude'],
        'lon': data['coordinates']['longitude'],
        'pm10': pm10,
        'pm25': pm25,
        'time': NOW
    })

sensors_df = pd.DataFrame(sensors).set_index('time')
print(sensors_df)
"""
try:
    client.write(sensors_df, data_frame_measurement_name='sensor',
                 data_frame_tag_columns=['name', 'id'])
except Exception as e:
    print(f"Error bij point: {e}")
time.sleep(2)
"""