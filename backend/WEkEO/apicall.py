import pandas as pd
import os
import netCDF4 as nc
from dotenv import load_dotenv
from hda import Client, Configuration
from influxdb_client_3 import InfluxDBClient3
from influxdb_client import InfluxDBClient
import pandas as pd
import netCDF4 as nc
import os
import numpy as np
from query import query_settings
import shutil

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = BASE_DIR+"./data"
NOW = pd.Timestamp.now(tz='UCT').strftime('%Y-%m-%d')

URL_INFLUDB = "http://localhost:8086"
ORG = "AP"
TOKEN = "I1SYSyvrMEmwP88EPLjxxxeQrk14TdIqid8Y4XmeEmqTveJczU5r9nb4x9l37JtXP0xt64-h5oZrplJN01jPMw=="
BUCKET = "WEkEO"

if os.path.exists(DATA_DIR):
    shutil.rmtree(DATA_DIR)

def get_locations(response):
    records = []
    sensor_ids = []
    for table in response:
        for record in table.records:
            records.append(record)
            if record.values["id"] not in sensor_ids:
                sensor_ids.append(record.values["id"])
                
    data = []
    for id in sensor_ids:
        sensor = {}
        for record in records:
            sensor.update({"id": id})
            if id == record.values["id"] and record.get_field() in ["lon", "lat"]:
                sensor.update({record.get_field(): record.get_value()})
        data.append(sensor)
    return data


def main():
    load_dotenv()
    config = Configuration(user=os.getenv("USERNAME_WEKEO"), password=os.getenv("PASSWORD"))
    hda_client = Client(config=config)
    write_client = InfluxDBClient3(host=URL_INFLUDB, token=TOKEN,
                            org=ORG, database=BUCKET, enable_gzip=True)
    
    read_client = InfluxDBClient(url=URL_INFLUDB, token=TOKEN, org=ORG)
    read_api = read_client.query_api()
    
    influxdb_query = """
            from(bucket: "BE-OpenAQ-sensors")
            |> range(start: 0)
            |> filter(fn: (r) => r["_measurement"] == "sensor")
            """
    
    response = read_api.query(influxdb_query, org=ORG)
    sensor_locations = get_locations(response)

    start_date = (pd.Timestamp(NOW, tz='UCT') - pd.DateOffset(1)).strftime('%Y-%m-%d')
    end_date = pd.Timestamp(NOW, tz='UCT').strftime('%Y-%m-%d')
    
    for i, sensor in enumerate(sensor_locations):
        print(f"searching lat: {sensor['lat']}, lon: {sensor['lon']}")
        query = query_settings(sensor['lat'], sensor['lon'], start_date, end_date)
        matches = hda_client.search(query)
        print("downloading data")
        matches.download(DATA_DIR)
    
        nc_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.nc')]
        data_file = nc.Dataset(f"{DATA_DIR}/{nc_files[i]}")

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
                'id': sensor['id'],
                'lon': data['longitude'][0],
                'lat': data['latitude'][0],
                'time': pd.Timestamp(f"{date}T{hour}:00:00.000Z")
            }
            
            for key in data_file.variables.keys():
                if key not in ['longitude', 'latitude', 'time', 'level']:
                    data_dict.update({key: data[key][i]})    
            wekeo.append(data_dict)
            
        print("sending data to database")
        wekeo_df = pd.DataFrame(wekeo).set_index('time')
        
        try:
            write_client.write(wekeo_df, data_frame_measurement_name='sensor', data_frame_tag_columns=['id'])
        except Exception as e:
            print(f"Error bij point: {e}")


if __name__ == "__main__":
    main()