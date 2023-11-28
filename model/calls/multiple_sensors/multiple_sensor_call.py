import requests
import pandas as pd
import time
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"/datasets"
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def process_sensor(sensor_id, type):
    URL_OPENAQ = f"https://airsight.cloudsin.space/api/{type}/{sensor_id}"
    HEADERS = {"accept": "application/json"}
    BODY = {
        "start_date": "2023-11-16T12:00:00.00",
        "stop_date": "2023-11-20T12:00:00.00"
    }

    response = requests.get(url=URL_OPENAQ, headers=HEADERS, json=BODY)

    sensors_list = []
    for data in response.json():
        if type == "openaqsensor":
            sensors_list.append({
                'sensor_id': data['id'],
                'local_date': data['time'],
                'lat': data['lat'],
                'lon': data['lon'],
                'no2': data.get('no2', None),
                'o3': data.get('o3', None),
                'pm10': data.get('pm10', None),
                'pm25': data.get('pm25', None),
                'so2': data.get('so2', None)
            })
        elif type == "wekeosensor":
            sensors_list.append({
                'sensor_id': data['id'],
                'local_date': data['time'],
                'lat': data['lat'],
                'lon': data['lon'],
                'co': data.get('co_conc', None),
                'no2': data.get('no2_conc', None),
                'o3': data.get('o3_conc', None),
                'pm10': data.get('pm10_conc', None),
                'pm25': data.get('pm2p5_conc', None),
                'so2': data.get('so2_conc', None)
            })

    sensors_df = pd.DataFrame(sensors_list)
    sensors_df = sensors_df.sort_values(by='local_date')
    if(type == "openaqsensor"):
        with open(DATA_DIR+'/openAQ_data.csv', 'a') as f:
            sensors_df.to_csv(f, header=f.tell()==0)
    elif(type == "wekeosensor"):
        with open(DATA_DIR+'/wekeo_data.csv', 'a') as f:
            sensors_df.to_csv(f, header=f.tell()==0)
    else:
        print("Error: type not found")

    print(sensors_df)

sensor_ids = [3036, 4463, 4861, 4926, 5698]

for sensor_id in sensor_ids:
    process_sensor(sensor_id, "openaqsensor")
    process_sensor(sensor_id, "wekeosensor")