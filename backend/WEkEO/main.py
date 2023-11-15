import netCDF4 as nc
from dotenv import load_dotenv
from hda import Client, Configuration
from pandas import Timestamp, DateOffset, DataFrame
from os import getenv, path, listdir
import numpy as np
from query import query_settings
from shutil import rmtree
from dotenv import load_dotenv
from requests import Session, get

load_dotenv()

USERNAME_WEKEO = getenv("USERNAME_WEKEO")
PASSWORD = getenv("PASSWORD")
API_URL = getenv("API_URL")

BASE_DIR = path.dirname(__file__)
DATA_DIR = f"{BASE_DIR}/data"
NOW = Timestamp.now(tz='UCT').strftime('%Y-%m-%d')


if path.exists(DATA_DIR):
    rmtree(DATA_DIR)

def get_sensor_locations(response):
    locations = []
    for sensor in response:
        locations.append({'id': sensor['id'], 'lon': sensor['lon'], 'lat': sensor['lat']})              
    return locations


def main():
    config = Configuration(user=USERNAME_WEKEO, password=PASSWORD)
    hda_client = Client(config=config)
    session = Session()
    
    try:
        response = get(f"{API_URL}/openaqsensor/").json()
    except Exception as e:
        print(f"Data not found: {e}")
        
    sensor_locations = get_sensor_locations(response)

    start_date = (Timestamp(NOW, tz='UCT') - DateOffset(1)).strftime('%Y-%m-%d')
    end_date = Timestamp(NOW, tz='UCT').strftime('%Y-%m-%d')
    
    for i, sensor in enumerate(sensor_locations):
        print(f"searching lat: {sensor['lat']}, lon: {sensor['lon']}")
        query = query_settings(sensor['lat'], sensor['lon'], start_date, end_date)
        matches = hda_client.search(query)
        
        print("downloading data")
        matches.download(DATA_DIR)
    
        nc_files = [f for f in listdir(DATA_DIR) if f.endswith('.nc')]
        data_file = nc.Dataset(f"{DATA_DIR}/{nc_files[i]}")

        data = {}
        for key in data_file.variables.keys():
            if key != "level":
                d = data_file.variables[key][:]
                normal_array = np.where(d.mask, None, d)
                result = [float(x) for x in normal_array.flatten() if x is not None]
            
                data.update({key: result})

        wekeo = []
        for i in range(len(data['time'])):
            hour = str(int(data['time'][i]) - (24 * (int(data['time'][i]) // 24)))
            if len(hour) == 1:
                hour = f"0{hour}"
            
            date = (Timestamp(start_date) + DateOffset((int(data['time'][i]) // 24))).strftime('%Y-%m-%d')

            data_dict = {
                'id': sensor['id'],
                'lon': data['longitude'][0],
                'lat': data['latitude'][0],
                'time': str(Timestamp(f"{date}T{hour}:00:00.000Z"))
            }
            
            for key in data_file.variables.keys():
                if key not in ['longitude', 'latitude', 'time', 'level']:
                    data_dict.update({key: data[key][i]})    
            wekeo.append(data_dict)
            
        print("sending data to database")
        wekeo_json = DataFrame(wekeo).to_json(orient="split")        
        print(session.post(f"{API_URL}/wekeosensor/new/", json={"data": wekeo_json}).json())


if __name__ == "__main__":
    main()