# this file is used to make api-calls to wekeo and store the data in a csv file  under datasets/wekeo_data.csv import pandas as pd
import os
import pandas as pd
import netCDF4 as nc
from .wekeo_query import query_settings
from dotenv import load_dotenv
from hda import Client, Configuration
from shutil import rmtree
from datetime import datetime, timedelta




def wekeo_api_call(start_date, end_date, lat, lon):
    ##Setup
    DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "datasets")
    DATA_DIR = os.path.join(DATASET_DIR, "temp_wekeo_data")

    load_dotenv()
    user_name= os.getenv("USERNAME_WEKEO")
    password= os.getenv("PASSWORD")
    config = Configuration(user=user_name, password=password) #username/password van je wekeo account meegeven
    hda_client = Client(config=config)

    query = query_settings(lat, lon, start_date, end_date)

    print("Query settings: ", query)
    matches = hda_client.search(query)
    print("Matches: ", matches)
    def read_nc_variables(DATA_DIR, variable_names, start_date):
        nc_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.nc')]
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
    df = df.rename(columns={"Time": "time", "pm10_conc": "pm10", "pm2p5_conc": "pm25", "no2_conc": "no2", "Local_date": "local_date", "nmvoc_conc": "nmvoc", "no_conc": "no", "o3_conc": "o3", "so2_conc": "so2"})
    df["time"] = df["time"] % 24
    df["time"] = df["time"].astype(int)
    df.to_csv(os.path.join(DATASET_DIR, "wekeo_data.csv"), index=False)

    if os.path.exists(DATA_DIR):
        try:
            rmtree(DATA_DIR)  
        except OSError as e:
            print(f"Error: {e}")
    else:
        print(f"Folder '{DATA_DIR}' does not exist.")

