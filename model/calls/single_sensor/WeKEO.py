import pandas as pd
import os
import json
import netCDF4 as nc
from dotenv import load_dotenv
from hda import Client, Configuration
from shutil import rmtree
from datetime import datetime, timedelta
from zipfile import ZipFile



BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"/wekeodata"
DATASET_DIR = BASE_DIR + "/datasets"
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')
##Setup
load_dotenv()
user_name= os.getenv("USERNAME_WEKEO")
password= os.getenv("PASSWORD")
config = Configuration(user=user_name, password=password) #username/password van je wekeo account meegeven
hda_client = Client(config=config)
start_date = "2023-10-02T00:00:00.000Z"

##The api call to wekeo (returns a zip file)
lat = 51.228629813460294
lon = 4.42845417753557
box = 0.05

bbox = [
    lon-box,
    lat-box,
    lon+box,
    lat+box
]

query = {
  "datasetId": "EO:ECMWF:DAT:CAMS_EUROPE_AIR_QUALITY_FORECASTS",
  "boundingBoxValues": [
    {
      "name": "area",
      "bbox": bbox
    }
  ],
  "dateRangeSelectValues": [
    {
      "name": "date",
      "start": start_date,
      "end": "2023-10-31T00:00:00.000Z"
    }
  ],
  "multiStringSelectValues": [
    {
      "name": "model",
      "value": [
        "ensemble"
      ]
    },
    {
      "name": "variable",
      "value": [
        "particulate_matter_10um",
        "particulate_matter_2.5um",
        "nitrogen_dioxide",
        "nitrogen_monoxide",
        "carbon_monoxide",
        "non_methane_vocs",
        "ozone",
        "sulphur_dioxide"
      ]
    },
    {
      "name": "type",
      "value": [
        "analysis"
      ]
    },
    {
      "name": "time",
      "value": [
        "08:00",
        "12:00",
        "16:00"
      ]
    },
    {
      "name": "level",
      "value": [
        "0"
      ]
    },
    {
      "name": "leadtime_hour",
      "value": [
        "0"
      ]
    }
  ],
  "stringChoiceValues": [
    {
      "name": "format",
      "value": "netcdf"
    }
  ]
}


matches= hda_client.search(query)
matches.download(DATA_DIR)


zip_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.zip')]
print(zip_files)

for zip_file in zip_files:
    with ZipFile(os.path.join(DATA_DIR, zip_file), 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
        
for zip_file in zip_files:
    os.remove(os.path.join(DATA_DIR, zip_file))
    

nc_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.nc')]

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

satellite_df = read_nc_variables(DATA_DIR, variable_names, start_date)
satellite_df = satellite_df.rename(columns={"Time": "time", "pm10_conc": "pm10", "pm2p5_conc": "pm25", "no2_conc": "no2", "Local_date": "local_date", "nmvoc_conc": "nmvoc", "no_conc": "no", "o3_conc": "o3", "so2_conc": "so2"})
satellite_df["time"] = satellite_df["time"] % 24
satellite_df["time"] = satellite_df["time"].astype(int)
satellite_df.to_csv(os.path.join(DATASET_DIR, "wekeo_data.csv"), index=False)

if os.path.exists(DATA_DIR):
    try:
        rmtree(DATA_DIR)  
    except OSError as e:
        print(f"Error: {e}")
else:
    print(f"Folder '{DATA_DIR}' does not exist.")