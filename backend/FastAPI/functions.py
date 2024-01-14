from pandas import Timestamp
from setup import BASE_QUERY, BUCKET, ORG, read_api, geo
from classes import Dates

# -----------Functions-----------


def records(response):
    data = {}
    for table in response:
        for record in table.records:
            data.update({record.get_field(): record.get_value()})
    return data


def check_dates(start_date, stop_date, dates):
    output_dates = Dates

    if start_date != None and stop_date != None and dates == None:
        if start_date == stop_date:
            stop_date = stop_date.split("T")[0] + "T23:00:00"
        output_dates.start_date = start_date + "Z"
        output_dates.stop_date = stop_date + "Z"
    elif dates != None:
        output_dates.start_date = f"{dates.start_date}Z"
        output_dates.stop_date = f"{dates.stop_date}Z"
    else:
        output_dates.start_date = None
        output_dates.stop_date = None

    return output_dates


def list_all_items(response):
    data = []
    for table in response:
        for record in table.records:
            item = {}
            for value in record.values:
                if value not in ["result", "table"]:
                    if record.values[value] is not None:
                        if value == '_time':
                            item.update({"time": record.values[value]})
                        else:
                            item.update({value: record.values[value]})
            data.append(item)
    return data


def get_query(param, dates, id=None, data=None):
    start_date, stop_date = dates.start_date, dates.stop_date

    if param in ["wekeo", "openaq"]:
        param += "sensor"
    measurement_filter = f"""|> filter(fn: (r) => r["_measurement"] == "{param}")"""

    id_filter = ""
    if id != None:
        id_filter = f"""|> filter(fn: (r) => r["id"] == "{id}")"""

    data_filter = ""
    if data != None:
        data_filter = f"""|> filter(fn: (r) => r["_field"] == "{data}")"""

    time_filter = f"""|> range(start: 0) |> last()"""
    if start_date != None and stop_date != None:
        time_filter = f"""|> range(start: {start_date}, stop: {stop_date})"""

    test_filter = f"""|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
                      |> group()
                      |> drop(columns: ["_start", "_stop", "_measurement",])"""

    return BASE_QUERY + time_filter + measurement_filter + id_filter + data_filter + test_filter


def get_address_by_location(latitude, longitude, language="en"):
    """This function returns an address as raw from a location
    will repeat until success"""
    coordinates = f"{latitude}, {longitude}"
    try:
        return geo.reverse(coordinates, language=language, timeout=10).raw
    except:
        return get_address_by_location(latitude, longitude)
