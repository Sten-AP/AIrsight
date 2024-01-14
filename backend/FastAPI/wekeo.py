from setup import BASE_DIR, WEKEO_URL, credentials
from netCDF4 import Dataset
from pandas import Timestamp, DateOffset, DataFrame
from os import path, listdir, mkdir
import numpy as np
from query import query_settings
from shutil import rmtree
from requests import Session
from time import sleep
from datetime import datetime, timedelta

DATA_DIR = f"{BASE_DIR}\\data"
VARIABLE_NAMES = ["pm10_conc", "pm2p5_conc", "no2_conc",
                  "o3_conc", "so2_conc", "co_conc", "nmvoc_conc", "no_conc"]


def start_and_end_date(days):
    start_date = (Timestamp.now(tz='UCT') -
                  DateOffset(days)).strftime('%Y-%m-%d')
    end_date = (Timestamp.now(tz='UCT') - DateOffset(0)).strftime('%Y-%m-%d')
    return [start_date, end_date]


def check_status(session, url, headers):
    while True:
        try:
            status_response = session.get(url, headers=headers).json()
            if status_response['status'] == 'completed':
                break
        except:
            print("Retry getting response")
        sleep(5)


def read_nc_variables(start_date):
    nc_files = [f for f in listdir(f"{DATA_DIR}") if f.endswith('.nc')]
    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    data_list = []
    for nc_file in nc_files:
        file = Dataset(path.join(DATA_DIR, nc_file))
        time_steps = file.variables['time'][:]

        for i, time_step in enumerate(time_steps):
            local_date = start_date + timedelta(hours=int(time_step))
            data_row = {'time': local_date.strftime(
                "%Y-%m-%dT%H:%M:%S+00:00"), 'hour': int(time_step)}
            for var_name in VARIABLE_NAMES:
                if var_name in file.variables:
                    data_row[var_name] = file.variables[var_name][i, 0, 0, 0]
            data_list.append(data_row)
        file.close()
    return DataFrame(data_list)


def conver_dataframe(df):
    weekday = datetime.fromisoformat(df["time"][0]).weekday() + 1
    month = datetime.fromisoformat(df["time"][0]).month
    data = {
        "pm25_x": df["pm25"][0],
        "pm10_x": df["pm10"][0],
        "no2_x": df["no2"][0],
        "so2": df["so2"][0],
        "co_conc": df["co_conc"][0],
        "hour_sin": [np.sin(2 * np.pi * df["hour"][0]/24)],
        "hour_cos": [np.cos(2 * np.pi * df["hour"][0]/24)],
        "day_of_week_sin": [np.sin(2 * np.pi * weekday/7)],
        "day_of_week_cos": [np.cos(2 * np.pi * weekday/7)],
        "month_sin": [np.sin(2 * np.pi * month/12)],
        "month_cos": [np.cos(2 * np.pi * month/12)]
    }
    return DataFrame(data)


def download_data(lat, lon, days=1):
    session = Session()
    if path.exists(DATA_DIR):
        rmtree(DATA_DIR)
    mkdir(DATA_DIR)
    date = start_and_end_date(days)

    print(f"[>] {date[0]} -> {date[1]} [<] searching lat: {lat}, lon: {lon}")
    token_response = session.get(f'{WEKEO_URL}/gettoken', headers={'Authorization': f'Basic {credentials}'}).json()
    headers = {'Authorization': token_response['access_token']}

    query = query_settings(lat, lon, date[0], date[1])
    matches = session.post(f'{WEKEO_URL}/datarequest',
                           headers=headers, json=query).json()
    jobId = matches['jobId']

    check_status(session, f'{WEKEO_URL}/datarequest/status/{jobId}', headers)
    results_response = session.get(f'{WEKEO_URL}/datarequest/jobs/{jobId}/result', headers=headers).json()
    sleep(2)

    print("downloading data")
    for result in results_response['content']:
        order_data = {
            "jobId": jobId,
            "uri": result['url']
        }
        order_response = session.post(f'{WEKEO_URL}/dataorder', headers=headers, json=order_data).json()
        sleep(2)

        check_status(session, f'{WEKEO_URL}/dataorder/status/{order_response["orderId"]}', headers)
        download_response = session.get(f'{WEKEO_URL}/dataorder/download/{order_response["orderId"]}', headers=headers, stream=True)

        with open(f"{DATA_DIR}/{order_response['orderId']}.nc", 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    df = read_nc_variables(f"{date[0]}T00:00:00.00Z")
    df = df.rename(columns={
        "pm10_conc": "pm10",
        "pm2p5_conc": "pm25",
        "no2_conc": "no2",
        "nmvoc_conc": "nmvoc",
        "no_conc": "no",
        "o3_conc": "o3",
        "so2_conc": "so2"
    })
    df["hour"] = df["hour"] % 24
    return conver_dataframe(df)
