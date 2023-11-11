from pandas import Timestamp, DataFrame
from dotenv import load_dotenv
import requests
import os
import schedule

load_dotenv()

response = requests.get(url=os.getenv("OPENAQ_URL"), headers={"accept": "application/json"})

def main():
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
    print(requests.post(os.getenv("API_URL") + f"/sensor/new/", json={"data": sensoren_json}).json())


if __name__ == "__main__":
    schedule.every().hour.do(main)
    while True:
        schedule.run_pending()
