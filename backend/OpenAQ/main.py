from pandas import Timestamp, DataFrame
from dotenv import load_dotenv
from requests import Session, get
from os import getenv
from time import sleep

load_dotenv()

OPENAQ_URL = getenv("OPENAQ_URL")
API_URL = getenv("API_URL")

def main():
    session = Session()
    while True:
        response = get(url=OPENAQ_URL, headers={"accept": "application/json"})
        sensoren = []
        timestamp = Timestamp.now(tz='UCT').floor('ms')
        for result in response.json()['results']:
            sensor = {
                'id': result['id'],
                'name': result['name'],
                'lat': result['coordinates']['latitude'],
                'lon': result['coordinates']['longitude'],
                'time': str(Timestamp(f"{timestamp.date()}T{timestamp.hour}:00:00.000Z"))
            }
            
            for parameter in result["parameters"]:
                if parameter["lastValue"] > -1:
                    sensor.update({parameter["parameter"]: parameter["lastValue"]})
            
            sensoren.append(sensor)
            
        sensoren_json = DataFrame(sensoren).to_json(orient="split")
        try:
            print(session.post(f"{API_URL}/openaqsensor/new/", json={"data": sensoren_json}).json())
        except Exception as e:
            print(f"Error posting data: {e}")
        sleep(1800)


if __name__ == "__main__":
    main()

