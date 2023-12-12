import requests
import pandas as pd
import os
from datetime import datetime, timedelta

URL_OPENAQ = "https://api.openaq.org/v2/measurements?format=json&date_from=2023-10-01T01%3A00%3A00-16%3A00&date_to=2023-10-31T08%3A00%3A00-16%3A00&page=1&offset=0&limit=100000&sort=desc&radius=1000&country=BE&location_id={}&order_by=datetime"

HEADERS = {"accept": "application/json"}

NOW = pd.Timestamp.now(tz='UCT').floor('ms')
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"/datasets"
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')

def fetch_sensor_data(sensor_id):
    response = requests.get(url=URL_OPENAQ.format(sensor_id), headers=HEADERS)
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
            sensors_dict[local_date]['latitude'] = data['coordinates']['latitude']
            sensors_dict[local_date]['longitude'] = data['coordinates']['longitude']
        else:
            sensors_dict[local_date] = {
                'pm10': pm10,
                'pm25': pm25,
                'no2': no2,
                'latitude': data['coordinates']['latitude'],
                'longitude': data['coordinates']['longitude']
            }
                
    for local_date, values in sensors_dict.items():
        local_date_converted = datetime.fromisoformat(local_date)
        offset_hours = local_date_converted.utcoffset().total_seconds() / 3600
        local_date_converted = local_date_converted + timedelta(hours=offset_hours)
        sensors_list.append({
            'time': local_date_converted.hour,
            'local_date': local_date_converted.replace(tzinfo=None).isoformat(),
            'sensor_id': sensor_id,
            'pm10': values['pm10'],
            'pm25': values['pm25'],
            'no2': values['no2'],
            'latitude': values['latitude'],
            'longitude': values['longitude']
        })

    sensors_df = pd.DataFrame(sensors_list).set_index('time')
    sensors_df = sensors_df.sort_values(by='local_date')

    # Check if file exists and is empty
    if os.path.exists(DATA_DIR+'/openAQ_data.csv') and os.path.getsize(DATA_DIR+'/openAQ_data.csv') > 0:
        # If file exists and is not empty, append without writing headers
        sensors_df.to_csv(DATA_DIR+'/openAQ_data.csv', mode='a', header=False)
    else:
        # If file doesn't exist or is empty, write with headers
        sensors_df.to_csv(DATA_DIR+'/openAQ_data.csv')

sensor_ids = [3036, 4463, 4861, 4926]
for sensor_id in sensor_ids:
    fetch_sensor_data(sensor_id)