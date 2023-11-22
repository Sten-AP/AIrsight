import requests
import pandas as pd
import time
import os
from datetime import datetime


#Interesting sensor id's: 4865 4867 4876 4879 4881

start_date = "2023-11-15T18:00:00.000Z"
end_date = "2023-11-17T18:00:00.000Z"

URL_FASTAPI = "https://airsight.cloudsin.space/api/openaqsensor/4865" 

HEADERS = {
    "accept": "application/json",
    "start_date": start_date,
    "stop_date": end_date
}

response = requests.get(url=URL_FASTAPI, headers=HEADERS)


NOW = pd.Timestamp.now(tz='UCT').floor('ms')
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"/datasets"
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')

print(response.json())


"""sensors_dict = {}  
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
    if datetime.fromisoformat(local_date).hour == 8 or datetime.fromisoformat(local_date).hour == 16 or datetime.fromisoformat(local_date).hour == 12:
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
        'local_date': local_date,
        'time': datetime.fromisoformat(local_date).hour,
        'pm10': values['pm10'],
        'pm25': values['pm25'],
        'no2': values['no2']
    })


sensors_df = pd.DataFrame(sensors_list).set_index('time')
sensors_df = sensors_df.sort_values(by='local_date')
sensors_df.to_csv(DATA_DIR+'/openAQ_data.csv')
print(sensors_df)"""

