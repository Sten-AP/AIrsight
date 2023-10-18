import pandas as pd
from zipfile import ZipFile
import os
import json
import netCDF4 as nc
from dotenv import load_dotenv
from hda import Client, Configuration

BASE_DIR = os.path.dirname(__file__)

##Setup
load_dotenv()
user_name= os.getenv("USERNAME_WEKEO")
password= os.getenv("PASSWORD")
config = Configuration(user=user_name, password=password) #username/password van je wekeo account meegeven
hda_client = Client(config=config)
dir_name = BASE_DIR+"./data"

print("============data download=============")
print(hda_client)

##The api call to wekeo (returns a zip file)
with open(BASE_DIR+'/query.json', 'r') as f:
    data = json.load(f)
print(data)

matches= hda_client.search(data)
matches.download(dir_name)


##Unzip the file
print("============zipfiles=============")
zip_files = [f for f in os.listdir(dir_name) if f.endswith('.zip')]
print(zip_files)

for zip_file in zip_files:
    with ZipFile(os.path.join(dir_name, zip_file), 'r') as zip_ref:
        zip_ref.extractall(dir_name)
        
for zip_file in zip_files:
    os.remove(os.path.join(dir_name, zip_file))
    
##Read the data
print("============ncfiles=============")
nc_files = [f for f in os.listdir(dir_name) if f.endswith('.nc')]

def read_nc_variabels (dir_name, variable_names, path_number):
        path =  dir_name + "/" + nc_files[path_number]
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

read_nc_variabels(dir_name, variable_names, -1)
