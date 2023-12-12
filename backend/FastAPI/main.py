from setup import app, write_client, read_api, ORG, PARAMETERS, BUCKET, geo, BASE_DIR
from classes import Data, Dates
from functions import get_query, list_all_items
from pandas import read_json
from uvicorn import run
from io import StringIO
import json
from fastapi import FastAPI, Query, Path, Depends
from enum import Enum
from pydantic.dataclasses import dataclass
from typing import Optional, List

# TIME FILTER FORMAT FOR REQUEST: 2023-11-15T12:00:00.00

params = ""
for i, param in enumerate(PARAMETERS):
    params += param
    if i != len(PARAMETERS)-1:
        params += ", "
        
enum = Enum("enum", {str(i):i for i in PARAMETERS})

# -----------Routes-----------
@app.post("/api/{param}/new/", tags=["Add item"], summary="Add new data to database")
async def add_new_data(data: Data, param: enum):
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


@app.get("/api/locations/", tags=["Latest data"], summary="Get all used locations")
async def locations():
    try:
        query = f"""import "influxdata/influxdb/v1"
                    v1.tagValues(
                        bucket: "{BUCKET}",
                        tag: "country_code",
                        start: 0
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

        query = f"""import "influxdata/influxdb/v1"
                    v1.tagValues(
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
            for val in country.values():
                country_code = val
            for key in country.keys():
                country_name = key

            country_data = {}
            regions = []
            for region in records_regions:
                locations = geo.geocode(region, country_codes=country_codes, language="en").raw["display_name"]
                locations = locations.split(", ")
                if locations[-1] == country_name:
                    regions.append(locations[0])
                country_data.update({"code": country_code})
                country_data.update({"regions": regions})
            data.append({country_name: country_data})
        return data
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/", tags=["Latest data"], summary="Get all latest data from all items from used parameter")
async def data_by_param(param: enum):
    param = param.value
    if param not in PARAMETERS:
        return {"error": "parameter does not match"}

    try:
        query = get_query(param)
        response = read_api.query(query, org=ORG)
        return list_all_items(response)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/{id}/", tags=["Specific data (with timestamps)"], summary="Get data from used parameter, filtered by id")
async def all_data_by_param_and_id(param: enum, id: str, dates: Dates = None):
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
        return list_all_items(response, start_date, stop_date)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/{param}/{id}/{data}/", tags=["Specific data (with timestamps)"], summary="Get specific data from used parameter, filtered by id")
async def specific_data_by_param_and_id(param: enum, id: str, data: str, dates: Dates = None):
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
        return list_all_items(response, start_date, stop_date)
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=6000, reload=True, proxy_headers=True, forwarded_allow_ips=['*'], workers=8)
