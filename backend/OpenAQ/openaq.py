import requests
import pandas as pd
from influxdb_client_3 import InfluxDBClient3
import os
from dotenv import load_dotenv
import schedule

load_dotenv()

ORG = "AP"
BUCKET = "BE-OpenAQ-sensors"
URL_INFLUDB = "http://localhost:8086"
TOKEN = os.getenv("TOKEN")

URL_OPENAQ = "https://api.openaq.org/v2/locations?limit=10000&page=1&offset=0&sort=desc&radius=1000&country_id=134&order_by=lastUpdated&dump_raw=false"
HEADERS = {"accept": "application/json"}

BASE_DIR = os.path.dirname(__file__)

response = requests.get(url=URL_OPENAQ, headers=HEADERS)
client = InfluxDBClient3(host=URL_INFLUDB, token=TOKEN, org=ORG, database=BUCKET, enable_gzip=True)

def main():
    sensors = []
    for result in response.json()['results']:
        sensor = {
            'name': result['name'],
            'id': result['id'],
            'lat': result['coordinates']['latitude'],
            'lon': result['coordinates']['longitude'],
            'time': pd.Timestamp.now(tz='UCT').floor('ms')
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


if __name__ == "__main__":
    schedule.every().hour.do(main)
    while True:
        schedule.run_pending()