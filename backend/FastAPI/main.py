from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
from pandas import read_json
from pydantic import BaseModel
from influxdb_client_3 import InfluxDBClient3
from influxdb_client import InfluxDBClient
from uvicorn import run
from dotenv import load_dotenv
from os import getenv
from io import StringIO

load_dotenv()

# -----------Constants-----------
REACT_URLS = getenv("FASTAPI_REACT_URLS")
INFLUXDB_URL = getenv("FASTAPI_INFLUXDB_URL")
TOKEN = getenv("FASTAPI_TOKEN")
ORG = getenv("FASTAPI_ORG")
BUCKET = getenv("FASTAPI_BUCKET")

BASE_QUERY = f"""from(bucket: "{BUCKET}") 
                |> range(start: 0)
              """

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
class Sensoren(BaseModel):
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

# -----------Routes-----------
@app.post("/openaqsensor/new/")
async def make_new_sensor(sensoren: Sensoren):
    data_df = read_json(StringIO(sensoren.data), orient="split").set_index('time')
    try:
        write_client.write(data_df, data_frame_measurement_name='openaqsensor',
                    data_frame_tag_columns=['country', 'id'])
        return {"message": f"sensordata succesfully added to database"}
    except Exception as e:
        return {"message": f"error with adding data to database: {e}"}

@app.post("/wekeosensor/new/")
async def make_new_sensor_from_wekeo(sensoren: Sensoren):
    data_df = read_json(StringIO(sensoren.data), orient="split").set_index('time')
    try:
        write_client.write(data_df, data_frame_measurement_name='wekeosensor',
                    data_frame_tag_columns=['id'])
        return {"message": f"sensordata from wekeo succesfully added to database"}
    except Exception as e:
        return {"message": f"error with adding data to database: {e}"}

@app.get("/{param}/")
async def list_of_wekeo_sensors(param: str):
    if param not in ["wekeosensor", "openaqsensor"]:
        return {"error": "parameter does not match"}
    try:
        response = read_api.query(BASE_QUERY+f"""|> filter(fn: (r) => r["_measurement"] == "{param}")""", org=ORG)
        return list_items(response)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=6000, reload=True)
