import requests
import pandas as pd
import time
import os


URL_OPENAQ = "https://api.openaq.org/v2/measurements?format=json&date_from=2023-10-05T08%3A00%3A00-16%3A00&date_to=2023-10-15T08%3A00%3A00-16%3A00&limit=2&page=1&offset=0&sort=desc&radius=1000&country=BE&location_id=4878&order_by=datetime"

HEADERS = {"accept": "application/json"}

NOW = pd.Timestamp.now(tz='UCT').floor('ms')
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"/data"
SENSOR_NAME = "BETR801"
SENSOR_ID = "4878"

response = requests.get(url=URL_OPENAQ, headers=HEADERS)
print(response.json())
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

with open(DATA_DIR+'\single_sensor_data.json', 'w') as file:
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

