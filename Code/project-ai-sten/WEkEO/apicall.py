from hda import Client, Configuration
import json
from datetime import datetime
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.cm import get_cmap
from matplotlib.axes import Axes

import zipfile, os

import warnings

config = Configuration(user="username", password="password") #username/password van je wekeo account meegeven
hda_client = Client(config=config)
dir_name = "./data"
extension = ".zip"



print("============data download=============")
print(hda_client)

##The api call to wekeo (returns a zip file)
with open('cams_european_air_quality_forecast_data_descriptor.json', 'r') as f:
    data = json.load(f)
print(data)

matches= hda_client.search(data)
matches.download(dir_name)

zip_files = [f for f in os.listdir(dir_name) if f.endswith('.zip')]

##Unzip the file
print("============zipfiles=============")
print(zip_files)


for zip_file in zip_files:
    with zipfile.ZipFile(os.path.join(dir_name, zip_file), 'r') as zip_ref:
        zip_ref.extractall(dir_name)