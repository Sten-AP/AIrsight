from geopy.geocoders import Nominatim
from dotenv import load_dotenv
from os import getenv, path
from influxdb_client_3 import InfluxDBClient3
from influxdb_client import InfluxDBClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


load_dotenv()

# -----------Constants-----------
INFLUXDB_URL = getenv("FASTAPI_INFLUXDB_URL")
TOKEN = getenv("FASTAPI_TOKEN")
ORG = getenv("FASTAPI_ORG")
BUCKET = getenv("FASTAPI_BUCKET")
BASE_QUERY = f"""from(bucket: "{BUCKET}")"""
PARAMETERS = ["openaq", "wekeo", "prediction"]
BASE_DIR = path.dirname(__file__)

# -----------InfluxDB-settings-----------
read_client = InfluxDBClient(url=INFLUXDB_URL, token=TOKEN, org=ORG)
write_client = InfluxDBClient3(host=INFLUXDB_URL, token=TOKEN, org=ORG, database=BUCKET)
read_api = read_client.query_api()
geo = Nominatim(user_agent="airsight")


# -----------App-settings-----------
app = FastAPI(
    title="AIrsight",
    summary="AIrsight API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Add item",
            "description": "Add new item to database. Data must be in body.",
        },
        {
            "name": "Latest data",
            "description": "Get latest data from all items.",
        },
        {
            "name": "Specific data (with timestamps)",
            "description": "Get data by param from specific item with or withouth timestamps. Timestamps must be in body.",
        },
    ]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
