import requests
import pandas as pd
import time
import os


URL_OPENAQ = "https://api.openaq.org/v2/measurements?format=json&date_from=2023-10-05T08%3A00%3A00-16%3A00&date_to=2023-10-15T08%3A00%3A00-16%3A00&limit=20&page=1&offset=0&sort=desc&radius=1000&country=BE&location_id=4878&order_by=datetime"

HEADERS = {"accept": "application/json"}

NOW = pd.Timestamp.now(tz='UCT').floor('ms')
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"/data"


response = requests.get(url=URL_OPENAQ, headers=HEADERS)
print(response.json())
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

with open(DATA_DIR+'\single_sensor_data.json', 'w') as file:
    file.write(str(response.text))

sensors = []
for data in response.json()['results']:
    pm10, pm25, no2 = -1, -1, -1
    local_date = data['date']['local']
    if data['parameter'] == 'pm10':
        pm10 = data['value']
    elif data['parameter'] == 'pm25':
        pm25 = data['value']
    elif data['parameter'] == 'no2':
        no2 = data['value']

    sensors.append({
        'pm10': pm10,
        'pm25': pm25,
        'no2': no2,
        'local_date': local_date
    })

sensors_df = pd.DataFrame(sensors).set_index('local_date')
print(sensors_df)

