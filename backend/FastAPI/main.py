from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pandas import read_json, Timestamp
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
    allow_origins=["*"],
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

def list_all_items(response, start_date = None, stop_date = None):
    records = []
    item_ids = []
    for table in response:
        for record in table.records:
            records.append(record)
            if record.values["id"] not in item_ids:
                item_ids.append(record.values["id"])

    if start_date == None and stop_date == None:
        data = []
        for id in item_ids:
            item = {}
            for record in records:
                item.update({"id": id})
                item.update({"time": record["_time"]})
                if id == record.values["id"]:
                    item.update({record.get_field(): record.get_value()})
            data.append(item)
        return data
    
    start_date = str(Timestamp(start_date, tz='UCT')).replace(" ", "T")
    stop_date = str(Timestamp(stop_date, tz='UCT')).replace(" ", "T")
    
    
    times = []
    for record in records:
        if record['_time'] not in times:
            times.append(record['_time'])
    
    data = []
    for time in times:
        item = {}
        for record in records:
            if time == record["_time"]:
                item.update({'id': record['id']})
                item.update({'time': str(record['_time']).replace(" ", "T")})
                item.update({record["_field"]: record["_value"]})
                if item not in data:
                    data.append(item)
    return data
    
def get_query(param, id = None, data = None, start_date = None, stop_date = None):
    measurement_filter = f"""|> filter(fn: (r) => r["_measurement"] == "{param}")"""
    
    id_filter = ""
    if id != None:
        id_filter = f"""|> filter(fn: (r) => r["id"] == "{id}")"""
    
    data_filter = ""
    if data != None:
        data_filter = f"""|> filter(fn: (r) => r["_field"] == "{data}")"""
    
    time_filter = f"""|> range(start: 0)"""
    if start_date != None and stop_date != None:
        time_filter = f"""|> range(start: {start_date}, stop: {stop_date})"""
        
    return BASE_QUERY + time_filter + measurement_filter + id_filter + data_filter

    
# -----------Routes-----------
@app.post("/api/{param}/new/")
async def add_new_item(param: str, data: Data):
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

@app.get("/api/{param}/")
async def list_items(param: str):
    if param not in ["wekeosensor", "openaqsensor"]:
        return {"error": "parameter does not match"}
    
    try:
        query = get_query(param)
        response = read_api.query(query, org=ORG)
        return list_all_items(response)
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/{param}/{id}/")
async def list_item_with_id(param: str, id: str, request: Request):
    if param not in ["wekeosensor", "openaqsensor"]:
        return {"error": "parameter does not match"}
    
    start_date = request.headers.get('start_date')
    stop_date = request.headers.get('stop_date')

    try:
        query = get_query(param=param, id=id, start_date=start_date, stop_date=stop_date)
        response = read_api.query(query, org=ORG)
        return list_all_items(response, start_date, stop_date)
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/{param}/{id}/{data}/")
async def list_data_of_item_with_id(param: str, id: str, data: str, request: Request):
    if param not in ["wekeosensor", "openaqsensor"]:
        return {"error": "parameter does not match"}
    
    start_date = request.headers.get('start_date')
    stop_date = request.headers.get('stop_date')
    
    try:
        query = get_query(param=param, id=id, data=data, start_date=start_date, stop_date=stop_date)
        response = read_api.query(query, org=ORG)
        return list_all_items(response, start_date, stop_date)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=6000, reload=True, proxy_headers=True)


