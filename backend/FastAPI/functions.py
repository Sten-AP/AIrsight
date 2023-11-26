from pandas import Timestamp
from setup import BASE_QUERY

# -----------Functions-----------
def records(response):
    data = {}
    for table in response:
        for record in table.records:
            data.update({record.get_field(): record.get_value()})
    return data

def list_all_items(response, start_date = None, stop_date = None):
    records = []
    item_ids = []
    for table in response:
        for record in table.records:
            records.append(record)
            if record.values["id"] not in item_ids:
                item_ids.append(record.values["id"])

    if start_date == None and stop_date == None:
        data = []
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
    
    data = []
    for time in times:
        item = {}
        for record in records:
            if time == record["_time"]:
                item.update({'id': record['id']})
                item.update({'time': str(record['_time']).replace(" ", "T")})
                item.update({record["_field"]: record["_value"]})
                if item not in data:
                    data.append(item)
    return data
    
def get_query(param, id = None, data = None, start_date = None, stop_date = None):
    measurement_filter = f"""|> filter(fn: (r) => r["_measurement"] == "{param}")"""
    
    id_filter = ""
    if id != None:
        id_filter = f"""|> filter(fn: (r) => r["id"] == "{id}")"""
    
    data_filter = ""
    if data != None:
        data_filter = f"""|> filter(fn: (r) => r["_field"] == "{data}")"""
    
    time_filter = f"""|> range(start: 0)"""
    if start_date != None and stop_date != None:
        time_filter = f"""|> range(start: {start_date}, stop: {stop_date})"""
        
    return BASE_QUERY + time_filter + measurement_filter + id_filter + data_filter