from pandas import Timestamp, DataFrame, DateOffset
from dotenv import load_dotenv
from requests import Session, get
from os import getenv
from time import sleep
from geopy.geocoders import Nominatim
from pprint import pprint
import threading

load_dotenv()

OPENAQ_URL = getenv("OPENAQ_INDIVIDUAL_URL")
API_URL = getenv("OPENAQ_API_URL")
SENSORS = ["4926", "4463", "3036", "4861", "3126"]
DAYS = 1


def get_address_by_location(latitude, longitude, language="en"):
    """This function returns an address as raw from a location
    will repeat until success"""
    coordinates = f"{latitude}, {longitude}"
    try:
        return geo.reverse(coordinates, language=language).raw
    except:
        return get_address_by_location(latitude, longitude)

def get_data(sensor_id):
    start_date = (Timestamp.now(tz='UCT') - DateOffset(DAYS)).strftime('%Y-%m-%d')
    end_date = (Timestamp.now(tz='UCT') - DateOffset(0)).strftime('%Y-%m-%d')
    print(f"[>] {start_date} -> {end_date} [<] searching sensor: {sensor_id}")

    response = get(url=OPENAQ_URL+f"?location_id={sensor_id}"+f"&date_from={start_date}" + f"&date_to={end_date}"+"&limit=1000", headers={"accept": "application/json"}).json()
    sensoren = []
    for result in response['results']:
        address = get_address_by_location(
            result['coordinates']['latitude'], result['coordinates']['longitude'])['address']

        if address.get("state") is not None:
            state = address["state"]
        else:
            state = address["region"]

        sensor = {
                'id': result['locationId'],
                'region': state,
                'country': address["country"],
                'country_code': address["country_code"].upper(),
                'lat': result['coordinates']['latitude'],
                'lon': result['coordinates']['longitude'],
                'time': result['date']['local']
            }

        sensor.update({result["parameter"]: result["value"]})

        sensoren.append(sensor)


    sensoren_json = DataFrame(sensoren).to_json(orient="split")
    try:
        print(session.post(f"{API_URL}/openaq/new/", json={"data": sensoren_json}).json())
    except Exception as e:
        print(f"Error posting data: {e}")


def main():
    for sensor_id in SENSORS:
        threading.Thread(target=get_data, args=(sensor_id,)).start()
        sleep(1)
        active_threads = threading.active_count()
        print(f"Threads active: {active_threads-1}")
        
if __name__ == "__main__":
    geo = Nominatim(user_agent="airsight")
    session = Session()
    main()
