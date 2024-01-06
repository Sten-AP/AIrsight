# this file is used to make api-calls to wekeo and store the data in a csv file  under datasets/wekeo_data.csv import pandas as pd
import base64
import os
import time
import pandas as pd
import netCDF4 as nc
import requests
from .wekeo_query import query_settings
from dotenv import load_dotenv
from shutil import rmtree
from datetime import datetime, timedelta




def wekeo_api_call(start_date, end_date, lat, lon, sensor_id):
    ##Setup
    DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "datasets")
    DATA_DIR = os.path.join(DATASET_DIR, "temp_wekeo_data")
    os.makedirs(DATA_DIR, exist_ok=True)

    load_dotenv()
    user_name= os.getenv("USERNAME_WEKEO")
    password= os.getenv("PASSWORD")
    credentials = base64.b64encode(f"{user_name}:{password}".encode()).decode()
    response = requests.get('https://wekeo-broker.prod.wekeo2.eu/databroker/gettoken', headers={'Authorization': f'Basic {credentials}'})
    access_token = response.json()['access_token']


    query = query_settings(lat, lon, start_date, end_date)

    headers = {'Authorization': access_token}
    response = requests.post('https://wekeo-broker.prod.wekeo2.eu/databroker/datarequest', headers=headers, json=query)
    matches = response.json()
    
    print("Matches: ", matches)
    jobId = matches['jobId']
    while True:
        response = requests.get(f'https://wekeo-broker.prod.wekeo2.eu/databroker/datarequest/status/{jobId}', headers=headers)
        status = response.json()['status']

        if status == 'completed':
            break

        time.sleep(5)

    response = requests.get(f'https://wekeo-broker.prod.wekeo2.eu/databroker/datarequest/jobs/{jobId}/result', headers=headers)
    results = response.json()
    print("Results: ", results)
    for result in results['content']:
        order_data = {
            "jobId": jobId,
            "uri": result['url']  
        }
        response = requests.post('https://wekeo-broker.prod.wekeo2.eu/databroker/dataorder', headers=headers, json=order_data)
        order = response.json()

        while True:
            response = requests.get(f'https://wekeo-broker.prod.wekeo2.eu/databroker/dataorder/status/{order["orderId"]}', headers=headers)
            status = response.json()['status']

            if status == 'completed':
                break

            time.sleep(5)

        response = requests.get(f'https://wekeo-broker.prod.wekeo2.eu/databroker/dataorder/download/{order["orderId"]}', headers=headers, stream=True)
        with open(os.path.join(DATA_DIR, f"{order['orderId']}.nc"), 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    
    def read_nc_variables(DATA_DIR, variable_names, start_date):
        nc_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.nc')]
        print(f"Found {len(nc_files)} .nc files in {DATA_DIR}")
        data_list = []  
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")  

        for nc_file in nc_files:
            file = nc.Dataset(os.path.join(DATA_DIR, nc_file))
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
        return pd.DataFrame(data_list)
        

    variable_names = ["pm10_conc", "pm2p5_conc", "no2_conc", "o3_conc", "so2_conc", "co_conc", "nmvoc_conc", "no_conc"]

    df = read_nc_variables(DATA_DIR, variable_names, start_date)
    print(df.columns)
    df = df.rename(columns={"Time": "time", "pm10_conc": "pm10", "pm2p5_conc": "pm25", "no2_conc": "no2", "Local_date": "local_date", "nmvoc_conc": "nmvoc", "no_conc": "no", "o3_conc": "o3", "so2_conc": "so2"})
    df["time"] = df["time"] % 24
    df["time"] = df["time"].astype(int)
    df['sensor_id'] = sensor_id 

    csv_file = os.path.join(DATASET_DIR, "wekeo_data.csv")
    if os.path.isfile(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, index=False)

    if os.path.exists(DATA_DIR):
        try:
            rmtree(DATA_DIR)  
        except OSError as e:
            print(f"Error: {e}")
    else:
        print(f"Folder '{DATA_DIR}' does not exist.")

