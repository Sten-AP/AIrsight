import netCDF4 as nc
from dotenv import load_dotenv
from hda import Client, Configuration
from pandas import Timestamp, DateOffset, DataFrame
from os import getenv, path, listdir, remove
import numpy as np
from query import query_settings
from shutil import rmtree
from dotenv import load_dotenv
from requests import Session, get
import threading
from time import sleep

load_dotenv()

USERNAME = getenv("WEKEO_USERNAME")
PASSWORD = getenv("WEKEO_PASSWORD")
API_URL = getenv("WEKEO_API_URL")

BASE_DIR = path.dirname(__file__)
DATA_DIR = f"{BASE_DIR}/data"
DAYS = 7


if path.exists(DATA_DIR):
    rmtree(DATA_DIR)

def get_sensor_locations():
    try:
        response = get(f"{API_URL}/openaqsensor/").json()
    except Exception as e:
        print(f"Data not found: {e}")
        
    locations = []
    for sensor in response:
        if sensor['id'] in ["4926", "4463", "3036", "4861", "5698"]:
            locations.append({'id': sensor['id'], 'lon': sensor['lon'], 'lat': sensor['lat']})              
    return locations

def start_and_end_date(days):
    start_date = (Timestamp.now(tz='UCT') - DateOffset(days)).strftime('%Y-%m-%d')
    end_date = (Timestamp.now(tz='UCT') - DateOffset(0)).strftime('%Y-%m-%d')
    return [start_date, end_date]

def download_data(id, lat, lon, days):
    date = start_and_end_date(days)
    
    print(f"[>] {date[0]} -> {date[1]} [<] searching lat: {lat}, lon: {lon}")
    query = query_settings(lat, lon, date[0], date[1])
    matches = hda_client.search(query)
        
    print("downloading data")
    matches.download(f"{DATA_DIR}/{id}")

def post_data(start_date):
    id_dirs = listdir(DATA_DIR)
    for id_dir in id_dirs:
        nc_files = [f for f in listdir(f"{DATA_DIR}/{id_dir}") if f.endswith('.nc')]
    
        for nc_file in nc_files:
            data_file = nc.Dataset(f"{DATA_DIR}/{id_dir}/{nc_file}")
            
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
                    'id': id_dir,
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
            print(Session().post(f"{API_URL}/wekeosensor/new/", json={"data": wekeo_json}).json())

def main():
    sensor_locations = get_sensor_locations()
    for sensor in sensor_locations:
        worker = threading.Thread(target=download_data, args=(sensor['id'], sensor['lat'],sensor['lon'], DAYS,))
        worker.start()
        sleep(1)
        active_threads = threading.active_count()
        print(f"Threads active: {active_threads}")

    while True:
        print(threading.active_count())
        if threading.active_count() == 2:
            break
        sleep(5)
    
    post_data(start_and_end_date(DAYS)[0])
    

if __name__ == "__main__":
    config = Configuration(user=USERNAME, password=PASSWORD)
    hda_client = Client(config=config, progress=True)
    main()
