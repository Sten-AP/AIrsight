from pandas import Timestamp, DataFrame
from dotenv import load_dotenv
from requests import Session, get
from os import getenv
from time import sleep
from geopy.geocoders import Nominatim

load_dotenv()

OPENAQ_URL = getenv("OPENAQ_URL")
API_URL = getenv("OPENAQ_API_URL")


def get_address_by_location(latitude, longitude, language="en"):
    """This function returns an address as raw from a location
    will repeat until success"""
    coordinates = f"{latitude}, {longitude}"
    try:
        return geo.reverse(coordinates, language=language).raw
    except:
        return get_address_by_location(latitude, longitude)


def main():
    session = Session()
    while True:
        response = get(url=OPENAQ_URL, headers={"accept": "application/json"})
        sensoren = []
        timestamp = Timestamp.now(tz='UCT').floor('ms')
        for result in response.json()['results']:
            address = get_address_by_location(
                result['coordinates']['latitude'], result['coordinates']['longitude'])['address']
            
            if address.get("state") is not None:
                state = address["state"]
            else:
                state = address["region"]
                
            sensor = {
                'id': result['id'],
                'region': state,
                'country': address["country"],
                'country_code': address["country_code"].upper(),
                'lat': result['coordinates']['latitude'],
                'lon': result['coordinates']['longitude'],
                'time': str(Timestamp(f"{timestamp.date()}T{timestamp.hour}:00:00.000Z"))
            }
            
            for parameter in result["parameters"]:
                if parameter["lastValue"] > -1:
                    sensor.update({parameter["parameter"]: parameter["lastValue"]})

            sensoren.append(sensor)
            
        sensoren_json = DataFrame(sensoren).to_json(orient="split")
        print(sensoren_json)
        try:
            print(session.post(f"{API_URL}/openaqsensor/new/", json={"data": sensoren_json}).json())
        except Exception as e:
            print(f"Error posting data: {e}")
        sleep(1800)


if __name__ == "__main__":
    geo = Nominatim(user_agent="airsight")
    main()

