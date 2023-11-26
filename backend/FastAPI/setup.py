from dotenv import load_dotenv
from os import getenv
from influxdb_client_3 import InfluxDBClient3
from influxdb_client import InfluxDBClient

load_dotenv()

# -----------Constants-----------
INFLUXDB_URL = getenv("FASTAPI_INFLUXDB_URL")
TOKEN = getenv("FASTAPI_TOKEN")
ORG = getenv("FASTAPI_ORG")
BUCKET = getenv("FASTAPI_BUCKET")
BASE_QUERY = f"""from(bucket: "{BUCKET}")"""
PARAMETERS = ["wekeosensor", "openaqsensor"]

# -----------InfluxDB-settings-----------
read_client = InfluxDBClient(url=INFLUXDB_URL, token=TOKEN, org=ORG)
write_client = InfluxDBClient3(host=INFLUXDB_URL, token=TOKEN, org=ORG, database=BUCKET)
read_api = read_client.query_api()
