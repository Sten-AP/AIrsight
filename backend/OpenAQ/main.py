from pandas import Timestamp, DataFrame
from dotenv import load_dotenv
from requests import Session, get
import os
import time

load_dotenv()

def main():
    session = Session()
    while True:
        response = get(url=os.getenv("OPENAQ_URL"), headers={"accept": "application/json"})
        sensoren = []
        timestamp = Timestamp.now(tz='UCT').floor('ms')
        for result in response.json()['results']:
            sensor = {
                'id': result['id'],
                'name': result['name'],
                'lat': result['coordinates']['latitude'],
                'lon': result['coordinates']['longitude'],
                'time': Timestamp(f"{timestamp.date()}T{timestamp.hour}:00:00.000Z")
            }
            
            for parameter in result["parameters"]:
                if parameter["lastValue"] > -1:
                    sensor.update({parameter["parameter"]: parameter["lastValue"]})
            
            sensoren.append(sensor)
            
        sensoren_json = DataFrame(sensoren).to_json(orient="split")
        print(session.post(os.getenv("API_URL") + f"/openaqsensor/new/", json={"data": sensoren_json}).json())
        time.sleep(3600)


if __name__ == "__main__":
    main()

