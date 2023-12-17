# this is the main file used for both doing calls and building models based on the data from the calls
# NOTE: make sure to have a .env file in the root of the project with the following variables: USERNAME_WEKEO: <your username>, PASSWORD: <your password>
import os
from code.wekeo import wekeo_api_call
from code.openAQ import fetch_sensor_data
from code.model import merge_and_train

#setup
DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datasets")

# cli for choosing between one custom sensor or multiple sensors
print("Welcome to AIrsight model building!")
print("Please choose between the following options:")
print("1. Build a model based on one custom sensor")
print("2. Build a model based on multiple sensors")
choice = int(input("Please enter your choice: "))
validChoice = False


while not validChoice:
    if (choice ==1): 
        print("Please enter the sensor id of the sensor you want to build a model for: ")
        sensor_id = input()
        if os.path.isfile(os.path.join(DATASET_DIR, f"{sensor_id}_openAQ_data.csv")):
            overwrite = input("We already found an OpenAQ CSV. Do you want to overwrite it with a new call? (yes/no): ")
            if overwrite.lower() == "yes":
                lat, lon = fetch_sensor_data(sensor_id,"2023-10-02", "2023-10-04" )
                print("finished fetching data for sensor: ", sensor_id)
        if os.path.isfile(os.path.join(DATASET_DIR, f"{sensor_id}_wekeo_data.csv")):
            overwrite = input("We already found a Wekeo CSV. Do you want to overwrite it with a new call? (yes/no): ")
            if overwrite.lower() == "yes":
                wekeo_api_call("2023-10-02T00:00:00.000000Z","2023-10-04T00:00:00.000000Z", lat, lon)
        merge_and_train()
        validChoice = True
    elif (choice ==2): 
        print("You've chosen multiple sensors, building a model with 5 sensors in belgium...")
        sensor_ids = [4878] #TO-DO: get 5 sensors in belgium
        for sensor_id in sensor_ids:
            lat, lon = fetch_sensor_data(sensor_id,"2023-10-02", "2023-10-04" )
            print("finished fetching data for sensor: ", sensor_id)
            wekeo_api_call("2023-10-02T00:00:00.000000Z","2023-10-04T00:00:00.000000Z", lat, lon)
            merge_and_train()
        validChoice = True
    else: 
        print("Please enter a valid choice")
        choice = input("Please enter your choice: ")



