from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pandas import read_json
from pydantic import BaseModel
from influxdb_client_3 import InfluxDBClient3
from influxdb_client import InfluxDBClient
from uvicorn import run
from dotenv import load_dotenv
from os import getenv
from io import StringIO

load_dotenv()

## TIME FILTER FORMAT: 2023-11-15T12:00:00.000Z

# -----------Constants-----------
REACT_URLS = getenv("FASTAPI_REACT_URLS")
INFLUXDB_URL = getenv("FASTAPI_INFLUXDB_URL")
TOKEN = getenv("FASTAPI_TOKEN")
ORG = getenv("FASTAPI_ORG")
BUCKET = getenv("FASTAPI_BUCKET")
BASE_QUERY = f"""from(bucket: "{BUCKET}")"""

# -----------InfluxDB-settings-----------
read_client = InfluxDBClient(url=INFLUXDB_URL, token=TOKEN, org=ORG)
write_client = InfluxDBClient3(host=INFLUXDB_URL, token=TOKEN, org=ORG, database=BUCKET)
read_api = read_client.query_api()


# -----------App-settings-----------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=REACT_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------Classes-----------
class Data(BaseModel):
    data: str


# -----------Functions-----------
def records(response):
    data = {}
    for table in response:
        for record in table.records:
            data.update({record.get_field(): record.get_value()})
    return data

def list_items(response):
    records = []
    item_ids = []
    for table in response:
        for record in table.records:
            records.append(record)
            if record.values["id"] not in item_ids:
                item_ids.append(record.values["id"])

    data = []
    for id in item_ids:
        item = {}
        for record in records:
            item.update({"id": id})
            if id == record.values["id"]:
                item.update({record.get_field(): record.get_value()})
        data.append(item)
    return data

def list_items_with_time(response):
    records = []
    item_ids = []
    for table in response:
        for record in table.records:
            records.append(record)
            if record.values["id"] not in item_ids:
                item_ids.append(record.values["id"])
    print(item_ids)
    
    
# -----------Routes-----------
@app.post("/{param}/new/")
async def add_new_item(data: Data, param: str):
    if param not in ["wekeosensor", "openaqsensor"]:
        return {"error": "parameter does not match"}
    
    data_df = read_json(StringIO(data.data), orient="split").set_index('time')
    try:
        if param == "openaqsensor":
            write_client.write(data_df, data_frame_measurement_name=param, data_frame_tag_columns=['country', 'id'])
        if param == "wekeosensor":
            write_client.write(data_df, data_frame_measurement_name=param, data_frame_tag_columns=['id'])
        return {"message": f"{param} data succesfully added to database"}
    except Exception as e:
        return {"message": f"error with adding {param} data to database: {e}"}

@app.get("/{param}/")
async def list_items(param: str):
    if param not in ["wekeosensor", "openaqsensor"]:
        return {"error": "parameter does not match"}
    
    try:
        time_filter = f"""|> range(start: 0)"""
        measurement_filter = f"""|> filter(fn: (r) => r["_measurement"] == "{param}")"""
        query = BASE_QUERY + time_filter + measurement_filter
        
        response = read_api.query(query, org=ORG)
        return list_items(response)
    except Exception as e:
        return {"error": str(e)}

@app.get("/{param}/{id}/")
async def list_item_with_id(param: str, id: str, request: Request):
    if param not in ["wekeosensor", "openaqsensor"]:
        return {"error": "parameter does not match"}
    start_date = request.headers.get('start_date')
    stop_date = request.headers.get('stop_date')
    try:
        time_filter = f"""|> range(start: {start_date}, stop: {stop_date})"""
        measurement_filter = f"""|> filter(fn: (r) => r["_measurement"] == "{param}")"""
        id_filter = f"""|> filter(fn: (r) => r["id"] == "{id}")"""
        query = BASE_QUERY + measurement_filter + id_filter
        if start_date != None and stop_date != None:
            query += time_filter
            
        response = read_api.query(query, org=ORG)
        return list_items_with_time(response)
    except Exception as e:
        return {"error": str(e)}

@app.get("/{param}/{id}/{data}/")
async def list_data_of_item_with_id(param: str, id: str, data: str, request: Request):
    if param not in ["wekeosensor", "openaqsensor"]:
        return {"error": "parameter does not match"}
    start_date = request.headers.get('start_date')
    stop_date = request.headers.get('stop_date')
    try:
        time_filter = f"""|> range(start: {start_date}, stop: {stop_date})"""
        measurement_filter = f"""|> filter(fn: (r) => r["_measurement"] == "{param}")"""
        id_filter = f"""|> filter(fn: (r) => r["id"] == "{id}")"""
        data_filter = f"""|> filter(fn: (r) => r["_field"] == "{data}")"""
        query = BASE_QUERY + measurement_filter + id_filter + data_filter
        if start_date != None and stop_date != None:
            query += time_filter
            
        response = read_api.query(query, org=ORG)
        return list_items_with_time(response)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=6000, reload=True)


