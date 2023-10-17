import pandas as pd
import zipfile, os
import json
import netCDF4 as nc
from dotenv import load_dotenv
from hda import Client, Configuration

##Setup
load_dotenv()
user_name= os.getenv("USERNAME_WEKEO")
password= os.getenv("PASSWORD")
config = Configuration(user=user_name, password=password) #username/password van je wekeo account meegeven
hda_client = Client(config=config)
dir_name = "./data"

print("============data download=============")
print(hda_client)

##The api call to wekeo (returns a zip file)
with open('cams_european_air_quality_forecast_data_descriptor.json', 'r') as f:
    data = json.load(f)
print(data)

matches= hda_client.search(data)
matches.download(dir_name)


##Unzip the file
print("============zipfiles=============")
zip_files = [f for f in os.listdir(dir_name) if f.endswith('.zip')]
print(zip_files)

for zip_file in zip_files:
    with zipfile.ZipFile(os.path.join(dir_name, zip_file), 'r') as zip_ref:
        zip_ref.extractall(dir_name)

##Read the data
print("============ncfiles=============")
nc_files = [f for f in os.listdir(dir_name) if f.endswith('.nc')]
nc_file_path = "./data/"+ nc_files[-1]
nc_file = nc.Dataset(nc_file_path)

variable_names = ["pm10_conc", "pm2p5_conc"]
variables_data = {}

for var_name in variable_names:
    if var_name in nc_file.variables:
        variables_data[var_name] = nc_file.variables[var_name][:]

nc_variables = nc_file.variables["pm10_conc"][:]
print(nc_file)
print(variables_data)

nc_file.close()
