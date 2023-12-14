# this is the main file used for both doing calls and building models based on the data from the calls
# NOTE: make sure to have a .env file in the root of the project with the following variables: USERNAME_WEKEO: <your username>, PASSWORD: <your password>
from code.wekeo import wekeo_api_call
from code.openAQ import fetch_sensor_data

#setup
# cli for choosing between one custom sensor or multiple sensors
print("Welcome to AIrsight model building!")
print("Please choose between the following options:")
print("1. Build a model based on one custom sensor")
print("2. Build a model based on multiple sensors")
choice = int(input("Please enter your choice: "))
validChoice = False
sensors = []
while not validChoice:
    if (choice ==1): 
        print("Please enter the sensor id of the sensor you want to build a model for: ")
        sensor_id = input()
        validChoice = True
    elif (choice ==2): 
        print("You've chosen multiple sensors, building a model with 5 sensors in belgium...")
        sensor_ids = [4878] #TO-DO: get 5 sensors in belgium
        for sensor_id in sensor_ids:
            lat, lon = fetch_sensor_data(sensor_id,"2023-10-02", "2023-10-04" )
            wekeo_api_call("2023-10-02T00:00:00.000000Z","2023-10-04T00:00:00.000000Z", lat, lon)
            validChoice = True
    else: 
        print("Please enter a valid choice")
        choice = input("Please enter your choice: ")



