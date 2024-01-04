from setup import DATA_DIR, WEKEO_URL, credentials
from netCDF4 import Dataset
from pandas import Timestamp, DateOffset, DataFrame
from os import  path, listdir, mkdir
import numpy as np
from query import query_settings
from shutil import rmtree
from requests import Session
from time import sleep
from datetime import datetime, timedelta


def start_and_end_date(days):
    start_date = (Timestamp.now(tz='UCT') -
                  DateOffset(days)).strftime('%Y-%m-%d')
    end_date = (Timestamp.now(tz='UCT') - DateOffset(0)).strftime('%Y-%m-%d')
    return [start_date, end_date]


def check_status(session, url, headers):
    while True:
        status_response = session.get(url, headers=headers).json()
        if status_response['status'] == 'completed':
            break
        sleep(5)

def read_nc_variables(DATA_DIR, variable_names, start_date):
    nc_files = [f for f in listdir(DATA_DIR) if f.endswith('.nc')]
    print(f"Found {len(nc_files)} .nc files in {DATA_DIR}")
    data_list = []
    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    for nc_file in nc_files:
        file = Dataset(path.join(DATA_DIR, nc_file))
        time_steps = file.variables['time'][:]
        print(file)

        for i, time_step in enumerate(time_steps):
            local_date = start_date + timedelta(hours=int(time_step))
            data_row = {'Time': time_step, 'Local_date': local_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")}
            for var_name in variable_names:
                if var_name in file.variables:
                    data_row[var_name] = file.variables[var_name][i, 0, 0, 0]
            data_list.append(data_row)
        file.close()
    return DataFrame(data_list)


def download_data(id, lat, lon, days):
    session = Session()
    if path.exists(DATA_DIR):
        rmtree(DATA_DIR)
    mkdir(DATA_DIR)
    date = start_and_end_date(days)

    print(f"[>] {date[0]} -> {date[1]} [<] searching lat: {lat}, lon: {lon}")
    token_response = session.get(
        f'{WEKEO_URL}/gettoken', headers={'Authorization': f'Basic {credentials}'}).json()
    headers = {'Authorization': token_response['access_token']}

    query = query_settings(lat, lon, date[0], date[1])
    matches = session.post(f'{WEKEO_URL}/datarequest',
                           headers=headers, json=query).json()
    jobId = matches['jobId']

    check_status(session, f'{WEKEO_URL}/datarequest/status/{jobId}', headers)
    results_response = session.get(
        f'{WEKEO_URL}/datarequest/jobs/{jobId}/result', headers=headers).json()

    print("downloading data")
    for result in results_response['content']:
        order_data = {
            "jobId": jobId,
            "uri": result['url']
        }
        order_response = session.post(
            f'{WEKEO_URL}/dataorder', headers=headers, json=order_data).json()

        check_status(session, f'{WEKEO_URL}/dataorder/status/{order_response["orderId"]}', headers)
        download_response = session.get(
            f'{WEKEO_URL}/dataorder/download/{order_response["orderId"]}', headers=headers, stream=True)

        if not path.exists(f"{DATA_DIR}/{id}"):
            mkdir(f"{DATA_DIR}/{id}")

        with open(f"{DATA_DIR}\\{id}\\{order_response['orderId']}.nc", 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    variable_names = ["pm10_conc", "pm2p5_conc", "no2_conc", "o3_conc", "so2_conc", "co_conc", "nmvoc_conc", "no_conc"]

    df = read_nc_variables(DATA_DIR, variable_names, start_and_end_date(days)[0])
    print(df.columns)
    # df = df.rename(columns={"Time": "time", "pm10_conc": "pm10", "pm2p5_conc": "pm25", "no2_conc": "no2",
    #                "Local_date": "local_date", "nmvoc_conc": "nmvoc", "no_conc": "no", "o3_conc": "o3", "so2_conc": "so2"})
    # df["time"] = df["time"] % 24
    # df["time"] = df["time"].astype(int)
    # df['id'] = id
    # df.to_csv(path.join(DATASET_DIR, "wekeo_data.csv"), index=False)


def predict(model):
    model.predict()
