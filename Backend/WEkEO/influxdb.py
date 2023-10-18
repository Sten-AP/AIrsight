import numpy as np
import datetime
import pandas as pd
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import netCDF4 as nc

file_name = '/filepath/RG_ArgoClim_Temperature_2019.nc'
data_structure = nc.Dataset(file_name)



print(data_structure.variables.keys())