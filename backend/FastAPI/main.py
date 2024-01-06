from setup import app, write_client, read_api, geo, model_pm10, model_pm25, ORG, PARAMETERS, PARAMETERS_ENUM, BUCKET, BASE_DIR
from wekeo import download_data
from fastapi.responses import ORJSONResponse
from classes import Data, Dates, Location
from functions import get_query, list_all_items
from pandas import read_json
from uvicorn import run
from io import StringIO
import json

index = 1

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
    id = f"request-{index}"

    data = download_data(location.lat, location.lon)
    prediction_pm10 = model_pm10.predict(data)[0]
    print(f"Prediction pm10: {prediction_pm10}")
    prediction_pm25 = model_pm25.predict(data)[0]
    print(f"Prediction pm2.5: {prediction_pm25}")
    try:
        # write_client.write(data_df, data_frame_measurement_name=f"prediction", data_frame_tag_columns=['id'])
        # index += 1
        return {"message": f"Prediction request succesfully added to database"}
    except Exception as e:
        return {"message": f"error with adding prediction request to database: {e}"}


@app.get("/api/locations/", tags=["Latest data"], summary="Get all used locations")
async def locations():
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

            data.append({country_name: country_data})
        return ORJSONResponse(data, status_code=200)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/", tags=["Latest data"], summary="Get all latest data from all items from used parameter")
async def data_by_param(param: PARAMETERS_ENUM):
    param = param.value
    if param not in PARAMETERS:
        return {"error": "parameter does not match"}

    try:
        query = get_query(param)
        response = read_api.query(query, org=ORG)
        return ORJSONResponse(list_all_items(response), status_code=200)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/{id}/", tags=["Specific data (with timestamps)"], summary="Get data from used parameter, filtered by id")
async def all_data_by_param_and_id(param: PARAMETERS_ENUM, id: str, dates: Dates = None):
    # TIME FILTER FORMAT FOR REQUEST: 2023-11-15T12:00:00
    param = param.value
    if param not in PARAMETERS:
        return {"error": "parameter does not match"}

    if dates != None:
        start_date = f"{dates.start_date}Z"
        stop_date = f"{dates.stop_date}Z"
    else:
        start_date = None
        stop_date = None

    try:
        query = get_query(param=param, id=id,
                          start_date=start_date, stop_date=stop_date)
        response = read_api.query(query, org=ORG)
        return ORJSONResponse(list_all_items(response, start_date, stop_date), status_code=200)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/{id}/{data}/", tags=["Specific data (with timestamps)"], summary="Get specific data from used parameter, filtered by id")
async def specific_data_by_param_and_id(param: PARAMETERS_ENUM, id: str, data: str, dates: Dates = None):
    # TIME FILTER FORMAT FOR REQUEST: 2023-11-15T12:00:00
    param = param.value
    if param not in PARAMETERS:
        return {"error": "parameter does not match"}

    if dates != None:
        start_date = f"{dates.start_date}Z"
        stop_date = f"{dates.stop_date}Z"
    else:
        start_date = None
        stop_date = None

    try:
        query = get_query(param=param, id=id, data=data,
                          start_date=start_date, stop_date=stop_date)
        response = read_api.query(query, org=ORG)
        return ORJSONResponse(list_all_items(response, start_date, stop_date), status_code=200)
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=5000, proxy_headers=True, forwarded_allow_ips=['*'], reload=True)
