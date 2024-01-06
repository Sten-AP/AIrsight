from geopy.geocoders import Nominatim
from dotenv import load_dotenv
from os import getenv, path
from influxdb_client_3 import InfluxDBClient3
from influxdb_client import InfluxDBClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI
from enum import Enum
import joblib
import base64


load_dotenv()

# -----------Constants-----------
INFLUXDB_URL = getenv("FASTAPI_INFLUXDB_URL")
TOKEN = getenv("FASTAPI_TOKEN")
ORG = getenv("FASTAPI_ORG")
BUCKET = getenv("FASTAPI_BUCKET")
BASE_QUERY = f"""from(bucket: "{BUCKET}")"""
PARAMETERS = ["openaq", "wekeo", "prediction"]
PARAMETERS_ENUM = Enum("Parameters", {str(i): i for i in PARAMETERS})
BASE_DIR = path.dirname(__file__)

WEKEO_URL = "https://wekeo-broker.prod.wekeo2.eu/databroker"
USERNAME = getenv("WEKEO_USERNAME")
PASSWORD = getenv("WEKEO_PASSWORD")
API_URL = getenv("WEKEO_API_URL")
DATA_DIR = f"{BASE_DIR}\\data"


# -----------InfluxDB-settings-----------
read_client = InfluxDBClient(url=INFLUXDB_URL, token=TOKEN, org=ORG)
write_client = InfluxDBClient3(
    host=INFLUXDB_URL, token=TOKEN, org=ORG, database=BUCKET)
read_api = read_client.query_api()
geo = Nominatim(user_agent="airsight")


# -----------WEkEO-settings-----------
credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()


# -----------Models-----------
model_pm10 = joblib.load(f"{BASE_DIR}/models/linear_regression_pm10.joblib")
model_pm25 = joblib.load(f"{BASE_DIR}/models/linear_regression_pm25.joblib")


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

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)
