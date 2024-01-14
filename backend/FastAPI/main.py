from setup import app, write_client, read_api, geo, model_no2, model_pm10, model_pm25, ORG, PARAMETERS, PARAMETERS_ENUM, BUCKET, BASE_DIR
from wekeo import download_data
from fastapi.responses import ORJSONResponse
from classes import Data, Dates, Location
from functions import get_query, list_all_items, get_address_by_location
from pandas import read_json, Timestamp, DataFrame
from uvicorn import run
from io import StringIO
import json


# -----------Routes-----------
@app.post("/api/{param}/new/", tags=["Add item"], summary="Add new data to database")
async def add_new_data(data: Data, param: PARAMETERS_ENUM):
    param = param.value
    if param not in PARAMETERS:
        return {"error": "parameter does not match"}

    data_df = read_json(StringIO(data.data), orient="split").set_index('time')
    try:
        if param == "openaq":
            write_client.write(data_df, data_frame_measurement_name="openaqsensor",
                               data_frame_tag_columns=['country', 'country_code', 'id', 'region'])
        if param == "wekeo":
            write_client.write(
                data_df, data_frame_measurement_name="wekeosensor", data_frame_tag_columns=['id'])
        return {"message": f"{param} data succesfully added to database"}
    except Exception as e:
        return {"message": f"error with adding {param} data to database: {e}"}


@app.post("/api/predict/", tags=["Add item"], summary="Get prediction of custom location")
async def custom_prediction(location: Location):
    index = f"{int(location.lat*10000)}{int(location.lon*10000)}"
    id = f"request-{index}"

    downloaded_data = download_data(location.lat, location.lon)
    prediction_no2 = model_no2.predict(downloaded_data)[0]
    prediction_pm10 = model_pm10.predict(downloaded_data)[0]
    prediction_pm25 = model_pm25.predict(downloaded_data)[0]

    timestamp = Timestamp.now(tz='UCT').floor('ms')
    address = get_address_by_location(location.lat, location.lon)['address']

    if address.get("state") is not None:
        state = address["state"]
    else:
        state = address["region"]

    data = {
        'id': id,
        'lat': float(location.lat),
        'lon': float(location.lon),
        'region': state,
        'country': address["country"],
        'country_code': address["country_code"].upper(),
        'no2': float(prediction_no2),
        'pm10': float(prediction_pm10),
        'pm25': float(prediction_pm25),
        'time': str(Timestamp(f"{timestamp.date()}T{timestamp.hour}:00:00.000Z"))
    }

    data_df = DataFrame([dict(data)]).set_index("time")
    try:
        write_client.write(data_df, data_frame_measurement_name=f"predictions",
                           data_frame_tag_columns=['country', 'country_code', 'id', 'region'])
        return {"message": f"Prediction {id} succesfully added to database"}
    except Exception as e:
        return {"message": f"error with adding prediction {id} to database: {e}"}


@app.get("/api/locations/", tags=["Latest data"], summary="Get all used locations")
async def locations():
    locations = json.load(open(f"{BASE_DIR}/locations.json", "r"))
    return ORJSONResponse(locations, status_code=200)

    try:
        query = f"""import "influxdata/influxdb/schema"
                    schema.tagValues(
                        bucket: "{BUCKET}",
                        tag: "country_code",
                        start: 0,
                    )"""
        response = read_api.query(query, org=ORG)

        country_codes = []
        for table in response:
            for record in table.records:
                country_codes.append(record.values['_value'])

        file = open(f"{BASE_DIR}/country_codes.json")
        country_codes_file = json.load(file)
        countries = []
        for country_code in country_codes:
            if country_code in country_codes_file:
                countries.append(
                    {country_codes_file[country_code]: country_code})
        file.close()

        query = f"""import "influxdata/influxdb/schema"
                    schema.tagValues(
                        bucket: "{BUCKET}",
                        tag: "region",
                        start: 0
                    )"""
        response = read_api.query(query, org=ORG)

        records_regions = []
        for table in response:
            for record in table.records:
                records_regions.append(record.values['_value'])

        data = []
        for country in countries:
            country_data = {}

            country_code = list(country.values())[0]
            country_name = list(country.keys())[0]
            country_data.update({"country": country_name})

            regions = []
            for region in records_regions:
                locations = geo.geocode(
                    region, country_codes=country_codes, language="en", timeout=10).raw["display_name"]
                locations = locations.split(", ")
                if locations[-1] == country_name:
                    regions.append(locations[0])
                country_data.update({"code": country_code})
                country_data.update({"regions": regions})

            data.append(country_data)
        return ORJSONResponse(data, status_code=200)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/", tags=["Latest data"], summary="Get all latest data from all items from used parameter")
async def data_by_param(param: PARAMETERS_ENUM, dates: Dates = None):
    param = param.value
    if param not in PARAMETERS:
        return {"error": "parameter does not match"}

    try:
        query = get_query(param=param, dates=dates)
        response = read_api.query(query, org=ORG)
        return ORJSONResponse(list_all_items(response, dates), status_code=200)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/{id}/", tags=["Specific data (with timestamps)"], summary="Get data from used parameter, filtered by id")
async def all_data_by_param_and_id(param: PARAMETERS_ENUM, id: str, dates: Dates = None):
    # TIME FILTER FORMAT FOR REQUEST: 2023-11-15T12:00:00
    param = param.value
    if param not in PARAMETERS:
        return {"error": "parameter does not match"}

    try:
        query = get_query(param=param, id=id, dates=dates)
        response = read_api.query(query, org=ORG)
        return ORJSONResponse(list_all_items(response, dates), status_code=200)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/{id}/{data}/", tags=["Specific data (with timestamps)"], summary="Get specific data from used parameter, filtered by id")
async def specific_data_by_param_and_id(param: PARAMETERS_ENUM, id: str, data: str, dates: Dates = None):
    # TIME FILTER FORMAT FOR REQUEST: 2023-11-15T12:00:00
    param = param.value
    if param not in PARAMETERS:
        return {"error": "parameter does not match"}

    try:
        query = get_query(param=param, id=id, data=data, dates=dates)
        response = read_api.query(query, org=ORG)
        return ORJSONResponse(list_all_items(response, dates), status_code=200)
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=5000,
        proxy_headers=True, forwarded_allow_ips=['*'], reload=True)
