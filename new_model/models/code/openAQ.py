# this file is used to make api-calls to openAQ and store the data in a csv file  under datasets/openAQ_data.csv
import requests
import pandas as pd
import os
from datetime import datetime, timedelta

URL_OPENAQ = "https://api.openaq.org/v2/measurements?format=json&date_from=2023-10-02T01%3A00%3A00-16%3A00&date_to=2023-10-4T08%3A00%3A00-16%3A00&page=1&offset=0&limit=100000&sort=desc&radius=1000&country=BE&location_id={}&order_by=datetime"
HEADERS = {"accept": "application/json"}
DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "datasets", "multiple_sensors")
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')

def fetch_sensor_data(sensor_id):
    response = requests.get(url=URL_OPENAQ.format(sensor_id), headers=HEADERS)
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
    sensors_df.to_csv(os.path.join(DATASET_DIR, "openAQ_data.csv"), index=False)
