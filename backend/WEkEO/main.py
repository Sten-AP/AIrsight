from netCDF4 import Dataset
from dotenv import load_dotenv
from pandas import Timestamp, DateOffset, DataFrame
from os import getenv, path, listdir, mkdir
import numpy as np
from query import query_settings
from shutil import rmtree
from dotenv import load_dotenv
from requests import Session
from time import sleep
import base64
import threading

load_dotenv()

USERNAME = getenv("WEKEO_USERNAME")
PASSWORD = getenv("WEKEO_PASSWORD")
API_URL = getenv("WEKEO_API_URL")
WEKEO_URL = "https://wekeo-broker.prod.wekeo2.eu/databroker"

BASE_DIR = path.dirname(__file__)
DATA_DIR = f"{BASE_DIR}/data"
SENSORS = ["4926", "4463", "3036", "4861", "3126", "72334"]
DAYS = 1


def get_sensor_locations():
    try:
        response = session.get(f"{API_URL}/openaq/").json()
    except:
        sleep(2)
        print("Retry getting sensorlocations")
        get_sensor_locations()

    locations = []
    for sensor in response:
        if sensor['id'] in SENSORS:
            locations.append(
                {'id': sensor['id'], 'lon': sensor['lon'], 'lat': sensor['lat']})
    return locations


def start_and_end_date(days):
    start_date = (Timestamp.now(tz='UCT') -
                  DateOffset(days)).strftime('%Y-%m-%d')
    end_date = (Timestamp.now(tz='UCT') - DateOffset(0)).strftime('%Y-%m-%d')
    return [start_date, end_date]


def check_status(url, headers):
    while True:
        try:
            status_response = session.get(url, headers=headers).json()
            if status_response['status'] == 'completed':
                break
        except:
            print("Retry getting response")
        sleep(5)


def download_data(id, lat, lon, days):
    session.post(f"{API_URL}/predict/", json={"lat": lat, "lon": lon})
    global index
    date = start_and_end_date(days)

    print(f"[>] {date[0]} -> {date[1]} [<] searching lat: {lat}, lon: {lon}")
    token_response = session.get(
        f'{WEKEO_URL}/gettoken', headers={'Authorization': f'Basic {credentials}'}).json()
    headers = {'Authorization': token_response['access_token']}

    query = query_settings(lat, lon, date[0], date[1])
    matches = session.post(f'{WEKEO_URL}/datarequest',
                           headers=headers, json=query).json()
    jobId = matches['jobId']

    check_status(f'{WEKEO_URL}/datarequest/status/{jobId}', headers)
    results_response = session.get(f'{WEKEO_URL}/datarequest/jobs/{jobId}/result', headers=headers).json()
    sleep(2)
    
    for result in results_response['content']:
        order_data = {
            "jobId": jobId,
            "uri": result['url']
        }
        
        order_response = session.post(f'{WEKEO_URL}/dataorder', headers=headers, json=order_data).json()
        sleep(2)

        check_status(f'{WEKEO_URL}/dataorder/status/{order_response["orderId"]}', headers)
            
        download_response = session.get(
            f'{WEKEO_URL}/dataorder/download/{order_response["orderId"]}', headers=headers, stream=True)

        if not path.exists(f"{DATA_DIR}/{id}"):
            mkdir(f"{DATA_DIR}/{id}")

        with open(f"{DATA_DIR}/{id}/{order_response['orderId']}.nc", 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    index += 1
    print(f"{index}/{len(SENSORS)} requests done ")


def post_data(start_date):
    id_dirs = listdir(DATA_DIR)
    for id_dir in id_dirs:
        nc_files = [f for f in listdir(
            f"{DATA_DIR}/{id_dir}") if f.endswith('.nc')]

        for nc_file in nc_files:
            data_file = Dataset(f"{DATA_DIR}/{id_dir}/{nc_file}")

            data = {}
            for key in data_file.variables.keys():
                if key != "level":
                    d = data_file.variables[key][:]
                    normal_array = np.where(d.mask, None, d)
                    result = [float(x)
                              for x in normal_array.flatten() if x is not None]

                    data.update({key: result})

            wekeo = []
            for i in range(len(data['time'])):
                hour = str(int(data['time'][i]) -
                           (24 * (int(data['time'][i]) // 24)))
                if len(hour) == 1:
                    hour = f"0{hour}"

                date = (Timestamp(
                    start_date) + DateOffset((int(data['time'][i]) // 24))).strftime('%Y-%m-%d')

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

            wekeo_json = DataFrame(wekeo).to_json(orient="split")
            try:
                print(session.post(
                    f"{API_URL}/wekeo/new/?sensor_id={id_dir}", json={"data": wekeo_json}).json())
            except Exception as e:
                print(f"Error posting data: {e}")


def main():
    while True:
        global index
        index = 0

        if path.exists(DATA_DIR):
            rmtree(DATA_DIR)
        mkdir(DATA_DIR)

        sensor_locations = get_sensor_locations()

        for sensor in sensor_locations:
            thread = threading.Thread(target=download_data, args=(
                sensor['id'], sensor['lat'], sensor['lon'], DAYS))
            thread.start()
            sleep(1)

        while index != len(SENSORS):
            sleep(10)

        post_data(start_and_end_date(DAYS)[0])
        sleep(7200)


if __name__ == "__main__":
    credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    session = Session()
    main()
