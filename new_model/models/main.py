# this is the main file used for both doing calls and building models based on the data from the calls
from code.wekeo import wekeo_api_call
from code.openAQ import fetch_sensor_data

#setup
# cli for choosing between one custom sensor or multiple sensors
print("Welcome to AIrsight model building!")
print("Please choose between the following options:")
print("1. Build a model based on one custom sensor")
print("2. Build a model based on multiple sensors")
choice = input("Please enter your choice: ")
sensors = []
if (choice ==1): 
    print("Please enter the sensor id of the sensor you want to build a model for: ")
    sensor_id = input()
elif (choice ==2): 
    print("You've chosen multiple sensors, building a model with 5 sensors in belgium...")
    sensor_ids = [3036, 4463, 4861, 4926, 4878]
    for sensor_id in sensor_ids:
        #TO-DO return lat and long from openaq to use in wekeo call
        fetch_sensor_data(sensor_id)
        wekeo_api_call("2023-10-02T00:00:00.000000Z","2023-10-04T00:00:00.000000Z", lat, lon)
else: 
    print("Please enter a valid choice")
    choice = input("Please enter your choice: ")



