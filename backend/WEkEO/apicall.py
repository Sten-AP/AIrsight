import pandas as pd
from zipfile import ZipFile
import os
import json
import netCDF4 as nc
from dotenv import load_dotenv
from hda import Client, Configuration

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"./data"
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')

##Setup
load_dotenv()
user_name= os.getenv("USERNAME_WEKEO")
password= os.getenv("PASSWORD")
config = Configuration(user=user_name, password=password) #username/password van je wekeo account meegeven
hda_client = Client(config=config)

print("============data download=============")
print(hda_client)

##The api call to wekeo (returns a zip file)
lat = 51.3
lon = 4.42
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
      "start": f"{NOW}T00:00:00.000Z",
      "end": f"{NOW}T00:00:00.000Z"
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
        "particulate_matter_2.5um",
        "particulate_matter_10um"
      ]
    },
    {
      "name": "type",
      "value": [
        "forecast"
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
        "0",
        "6",
        "12",
        "18",
        "24",
        "30",
        "36",
        "42",
        "48",
        "54",
        "60",
        "66",
        "72"
      ]
    },
    {
      "name": "time",
      "value": [
        "00:00"
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


##Unzip the file
print("============zipfiles=============")
zip_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.zip')]
print(zip_files)

for zip_file in zip_files:
    with ZipFile(os.path.join(DATA_DIR, zip_file), 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
        
for zip_file in zip_files:
    os.remove(os.path.join(DATA_DIR, zip_file))
    
##Read the data
print("============ncfiles=============")
nc_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.nc')]

def read_nc_variabels (DATA_DIR, variable_names, path_number):
        path =  DATA_DIR + "/" + nc_files[path_number]
        file = nc.Dataset(path)

        variables_data = {}

        for var_name in variable_names:
            if var_name in file.variables:
                variables_data[var_name] = file.variables[var_name][:]

        print(file)
        print(variables_data)
        file.close()


variable_names = ["pm10_conc", "pm2p5_conc"]
variables_data = {}

read_nc_variabels(DATA_DIR, variable_names, -1)
