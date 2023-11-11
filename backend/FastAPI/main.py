from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
from pandas import read_json
from pydantic import BaseModel
from influxdb_client_3 import InfluxDBClient3
from influxdb_client import InfluxDBClient
from uvicorn import run
from dotenv import load_dotenv
import os

load_dotenv()

# -----------Constants-----------
ORG = "AP"
BUCKET = "airsight"
BASE_QUERY = f"""from(bucket: "{BUCKET}") 
                |> range(start: 0)
                |> filter(fn: (r) => r["_measurement"] == "sensor")"""


# -----------InfluxDB-settings-----------
read_client = InfluxDBClient(url=os.getenv("INFLUXDB_URL"), token=os.getenv("TOKEN"), org=ORG)
write_client = InfluxDBClient3(host=os.getenv("INFLUXDB_URL"), token=os.getenv("TOKEN"), org=ORG, database=BUCKET)
read_api = read_client.query_api()


# -----------App-settings-----------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("REACT_URLS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------Classes-----------
class Sensoren(BaseModel):
    data: str


# -----------Functions-----------
def records(response):
    gegevens = {}
    for table in response:
        for record in table.records:
            gegevens.update({record.get_field(): record.get_value()})
    return gegevens


# -----------Routes-----------
@app.post("/sensor/new/")
async def make_new_sensor(sensoren: Sensoren):
    data_df = read_json(sensoren.data, orient="split").set_index('time')
    try:
        write_client.write(data_df, data_frame_measurement_name='sensor',
                    data_frame_tag_columns=['name', 'id'])
        return {"message": f"sensordata succesfully added to database"}
    except Exception as e:
        return {"message": f"error with adding data to database: {e}"}

@app.post("/wekeosensor/new/")
async def make_new_sensor_from_wekeo(sensoren: Sensoren):
    data_df = read_json(sensoren.data, orient="split").set_index('time')
    try:
        write_client.write(data_df, data_frame_measurement_name='wekeosensor',
                    data_frame_tag_columns=['id'])
        return {"message": f"sensordata from wekeo succesfully added to database"}
    except Exception as e:
        return {"message": f"error with adding data to database: {e}"}


@app.get("/sensor/")
async def list_of_sensors():
    try:
        response = read_api.query(BASE_QUERY, org=ORG)

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
                if id == record.values["id"]:
                    sensor.update({record.get_field(): record.get_value()})
            data.append(sensor)

        return data
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=6000, reload=True)
