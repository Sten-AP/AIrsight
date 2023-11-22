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

def process_sensor(sensor_id):
    URL_OPENAQ = f"https://api.openaq.org/v2/measurements?format=json&date_from=2023-10-01T01%3A00%3A00-16%3A00&date_to=2023-10-31T08%3A00%3A00-16%3A00&page=1&offset=0&limit=100000&sort=desc&radius=1000&country=BE&location_id={sensor_id}&order_by=datetime"
    HEADERS = {"accept": "application/json"}

    response = requests.get(url=URL_OPENAQ, headers=HEADERS)

    sensors_dict = {}  
    sensors_list = []
    for data in response.json()['results']:
        pm10, pm25, no2 = -1, -1, -1
        local_date = data['date']['local']

        if data['parameter'] == 'pm10':
            pm10 = data['value']
        elif data['parameter'] == 'pm25':
            pm25 = data['value']
        elif data['parameter'] == 'no2':
            no2 = data['value']
        if datetime.fromisoformat(local_date).hour in [8, 12, 16]:
            if local_date in sensors_dict:
                sensors_dict[local_date]['pm10'] = max(sensors_dict[local_date]['pm10'], pm10)
                sensors_dict[local_date]['pm25'] = max(sensors_dict[local_date]['pm25'], pm25)
                sensors_dict[local_date]['no2'] = max(sensors_dict[local_date]['no2'], no2)
            else:
                sensors_dict[local_date] = {
                    'pm10': pm10,
                    'pm25': pm25,
                    'no2': no2
                }
                
    for local_date, values in sensors_dict.items():
        sensors_list.append({
            'sensor_id': sensor_id,
            'local_date': local_date,
            'time': datetime.fromisoformat(local_date).hour,
            'pm10': values['pm10'],
            'pm25': values['pm25'],
            'no2': values['no2']
        })

    sensors_df = pd.DataFrame(sensors_list).set_index('time')
    sensors_df = sensors_df.sort_values(by='local_date')
    with open(DATA_DIR+'/openAQ_data.csv', 'a') as f:
        sensors_df.to_csv(f, header=f.tell()==0)
    print(sensors_df)

sensor_ids = [4865, 4867, 4876, 4879, 4881]

for sensor_id in sensor_ids:
    process_sensor(sensor_id)