from pandas import Timestamp, DataFrame
from dotenv import load_dotenv
from requests import Session
import os
import time

load_dotenv()

def main():
    session = Session()
    while True:
        response = session.get(url=os.getenv("OPENAQ_URL"), headers={"accept": "application/json"})
        sensoren = []
        for result in response.json()['results']:
            sensor = {
                'id': result['id'],
                'name': result['name'],
                'lat': result['coordinates']['latitude'],
                'lon': result['coordinates']['longitude'],
                'time': str(Timestamp.now(tz='UCT').floor('ms'))
            }
            
            for parameter in result["parameters"]:
                if parameter["lastValue"] > -1:
                    sensor.update({parameter["parameter"]: parameter["lastValue"]})
            
            sensoren.append(sensor)
            
        sensoren_json = DataFrame(sensoren).to_json(orient="split")
        print(session.post(os.getenv("API_URL") + f"/openaqsensor/new/", json={"data": sensoren_json}).json())
        time.sleep(1800)


if __name__ == "__main__":
    main()

