import pandas as pd
import os
import netCDF4 as nc
from dotenv import load_dotenv
from hda import Client, Configuration
from influxdb_client_3 import InfluxDBClient3
import pandas as pd
import time
import netCDF4 as nc
import os
import numpy as np
from query import query_settings

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"./data"
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')

URL_INFLUDB = "http://localhost:8086"
ORG = "AP"
TOKEN = "I1SYSyvrMEmwP88EPLjxxxeQrk14TdIqid8Y4XmeEmqTveJczU5r9nb4x9l37JtXP0xt64-h5oZrplJN01jPMw=="
BUCKET = "WEkEO"

def main():
    load_dotenv()
    config = Configuration(user=os.getenv("USERNAME_WEKEO"), password=os.getenv("PASSWORD")) #username/password van je wekeo account meegeven
    hda_client = Client(config=config)
    client = InfluxDBClient3(host=URL_INFLUDB, token=TOKEN,
                            org=ORG, database=BUCKET, enable_gzip=True)
     
     
    lat = 51.281014
    lon = 4.329848
      
    start_date = (pd.Timestamp(NOW) - pd.DateOffset(2)).strftime('%Y-%m-%d')
    end_date = pd.Timestamp(NOW).strftime('%Y-%m-%d')
    
    query = query_settings(lat, lon, start_date, end_date)
    
    print("============searching data=============")
    matches = hda_client.search(query)
    print("============data download=============")
    matches.download(DATA_DIR)
    
    nc_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.nc')]
    data_file = nc.Dataset(f"{DATA_DIR}/{nc_files[0]}")

    data = {}
    for key in data_file.variables.keys():
        if key != "level":
          d = data_file.variables[key][:]
          normal_array = np.where(d.mask, None, d)
          result = [float(x) for x in normal_array.flatten() if x is not None]
          
          data.update({key: result})

    wekeo = []
    for i in range(len(data['time'])):
        hour = str(int(data['time'][i]) - (24 * (int(data['time'][i]) // 24)))
        if len(hour) == 1:
            hour = f"0{hour}"
        
        date = (pd.Timestamp(start_date) + pd.DateOffset((int(data['time'][i]) // 24))).strftime('%Y-%m-%d')

        data_dict = {
            'lon': data['longitude'][0],
            'lat': data['latitude'][0],
            'time': pd.Timestamp(f"{date}T{hour}:00:00.000Z")
        }
        
        for key in data_file.variables.keys():
            if key not in ['longitude', 'latitude', 'time', 'level']:
                data_dict.update({key: data[key][i]})    
        wekeo.append(data_dict)
        
    print("============data to database=============")
    wekeo_df = pd.DataFrame(wekeo).set_index('time')

    try:
        client.write(wekeo_df, data_frame_measurement_name='satellite')
    except Exception as e:
        print(f"Error bij point: {e}")
    time.sleep(2)

if __name__ == "__main__":
    main()
