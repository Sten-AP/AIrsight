import requests
import pandas as pd
import time
import os
from datetime import datetime


URL_OPENAQ = "https://api.openaq.org/v2/measurements?format=json&date_from=2023-10-01T01%3A00%3A00-16%3A00&date_to=2023-10-14T08%3A00%3A00-16%3A00&page=1&offset=0&limit=1000&sort=desc&radius=1000&country=BE&location_id=4878&order_by=datetime"

HEADERS = {"accept": "application/json"}

NOW = pd.Timestamp.now(tz='UCT').floor('ms')
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"/datasets"
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')


response = requests.get(url=URL_OPENAQ, headers=HEADERS)
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

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
        'time': datetime.fromisoformat(local_date).hour,
        'pm10': values['pm10'],
        'pm25': values['pm25'],
        'no2': values['no2']
    })


sensors_df = pd.DataFrame(sensors_list).set_index('time')
sensors_df.to_csv(DATA_DIR+'/openAQ_data.csv')
print(sensors_df)

