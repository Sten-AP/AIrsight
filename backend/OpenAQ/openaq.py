import requests
import pandas as pd
from influxdb_client_3 import InfluxDBClient3
import time
import os
from dotenv import load_dotenv

load_dotenv()

ORG = "AP"
BUCKET = "BE-OpenAQ-sensors"
URL_INFLUDB = "http://localhost:8086"
TOKEN = os.getenv("TOKEN")

URL_OPENAQ = "https://api.openaq.org/v2/locations?limit=10000&page=1&offset=0&sort=desc&radius=1000&country_id=134&order_by=lastUpdated&dump_raw=false"
HEADERS = {"accept": "application/json"}

NOW = pd.Timestamp.now(tz='UCT').floor('ms')
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"/data"

response = requests.get(url=URL_OPENAQ, headers=HEADERS)
client = InfluxDBClient3(host=URL_INFLUDB, token=TOKEN, org=ORG, database=BUCKET, enable_gzip=True)

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

with open(DATA_DIR+'\openaq_data.json', 'w') as file:
    file.write(str(response.text))

def main():
    sensors = []
    for result in response.json()['results']:
        sensor = {
            'name': result['name'],
            'id': result['id'],
            'lat': result['coordinates']['latitude'],
            'lon': result['coordinates']['longitude'],
            'time': NOW
        }
        
        for parameter in result["parameters"]:
            if parameter["lastValue"] > -1:
                sensor.update({parameter["parameter"]: parameter["lastValue"]})

        sensors.append(sensor)

    sensors_df = pd.DataFrame(sensors).set_index('time')
    print(sensors_df)
    try:
        client.write(sensors_df, data_frame_measurement_name='sensor',
                    data_frame_tag_columns=['name', 'id'])
    except Exception as e:
        print(f"Error bij point: {e}")
    time.sleep(2)

if __name__ == "__main__":
    main()