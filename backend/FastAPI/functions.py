from pandas import Timestamp
from setup import BASE_QUERY, geo
from classes import Dates

# -----------Functions-----------
def records(response):
    data = {}
    for table in response:
        for record in table.records:
            data.update({record.get_field(): record.get_value()})
    return data


def check_dates(start_date, stop_date, dates):
    dates = Dates
    
    if start_date != None and stop_date != None and dates == None:
        dates.start_date = start_date
        dates.stop_date = stop_date
    elif dates != None:
        dates.start_date = f"{dates.start_date}Z"
        dates.stop_date = f"{dates.stop_date}Z"
    else:
        dates.start_date = None
        dates.stop_date = None
        
    return dates

def list_all_items(response, dates):
    start_date, stop_date = dates.start_date, dates.stop_date
    
    data = []
    records = []
    item_ids = []
    for table in response:
        for record in table.records:
            records.append(record)
            if record.values["id"] not in item_ids:
                item_ids.append(record.values["id"])

    if start_date == None and stop_date == None:
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
                
    for id in item_ids:
        for time in times:
            item = {}
            for record in records:
                if time == record["_time"]:
                    item.update({'id': id})
                    item.update({'time': str(record['_time']).replace(" ", "T")})
                    if id == record.values["id"]:
                        item.update({record.get_field(): record.get_value()})
                    if item not in data:
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

    return BASE_QUERY + time_filter + measurement_filter + id_filter + data_filter


def get_address_by_location(latitude, longitude, language="en"):
    """This function returns an address as raw from a location
    will repeat until success"""
    coordinates = f"{latitude}, {longitude}"
    try:
        return geo.reverse(coordinates, language=language, timeout=10).raw
    except:
        return get_address_by_location(latitude, longitude)
