# Model Documentation

On average the satellite's airquality values are inconsistent and sometimes outright wrong.

To solve that problem we've trained a model that corrects the satellite's readings in order to get more accurate and realistic results.

To correct said values we're using a linear regression model and the sensor's data as target data, since the sensor's are more accurate when it comes to air quality.

## The Structure of the data

### Model

A general summary of the model's used data:

- training data = wekeo's data (a.k.a. the satellite's data)
- test data= openAQ's data (a.k.a. the sensor's data)

### Datasets

For both the single senor model and the multiple sensor model we're using the "merged_data.csv" to train and test the model with

This is a combination of both datasets (openAQ's dataset and wekeo's dataset) and it exists of multiple fields regarding air quality:
sensor_id_x,local_date,lat_x,lon_x,co,no2_x,o3_x,pm10_x,pm25_x,so2_x,sensor_id_y,lat_y,lon_y,no2_y,o3_y,pm10_y,pm25_y,so2_y

- sensor_id
- local_date (on this field we've merged both datasets with an inner join)
- latitude
- longtitude
- Carbon Monoxide (co)
- Nitrogen Dioxide (no2)
- o3 (Ozone)
- pm10 (particulate matter and it's size: 10 microns)
- pm25 (particulate matter and it's size: 2.5 microns)
- o2 (Oxygen)

**_in the actual dataset you're likely to see this values with an "x" or "y" at the end. these stands for where the data came from: x means wekeo, y means openaq_**

## Project Infrastructure

model/
│ ├── calls
│ ├──── multiple_sensors
│ ├──── single_sensor
│ ├── model_building
│ ├───── correlations
│ ├───── multiple_sensors
│ └───── single_sensor

### Calls

In the calls folder we make get requests to the revelant api's and make/store datasets we'll use to base the model off.

#### single_sensor

The single sensor consists of two seperate python files that each make a call to the relevant api (wekeo's api and openAQ's api).

We format the result json and save them both as .csv's

#### multiple_sensors

The multiple sensors folder exists of a single python file that makes a call to our self-made fastAPI. It queries our database and returns both the wekeo and openAQ's data in one go. It still returns 2 .csv's, one for wekeo and one for openAQ.

#### Remarks

in both datasets folders, you might see a "merged_data.csv". During our model development (refer to model_building) we merge both datasets we made with the api calls into one via an inner join.

### model_building

#### correlations

In this folder we print out the correlations between all the different variables in our dataset (which variables stick well together and which are the best combinations for certain variables to get the best accuracy results).

The results found from the correlations tests are documented in a README.md file within the folder.

#### multiple_sensors

In multiple_sensors we develop the linear regression model based on the previously mentioned datasets.

It exists of one python file and a folder to store models for each relevant variable (pm10, pm25 and no2).

In both the single sensor folder and the multiple sensor model we merge de relevant datasets into with local_date (timestamp) as the index/joinpoint

#### single_sensor

Much like the previous folder, single sensor only exists of one python file and a folder to save models.

The main difference between these models is the data.

Single sensor is trained the data of one single sensor

Multiple sensors much like the name suggests is trained on multiple different sensors.

#### Remarks about the model(s)

The models are relatively similiar, the main differences are the amount of data, the amount of sensors and some added variables.

for pm10 and pm25 the training accuracies and test accuracies are on average in the mid range of 90%

(

- single sensor test accuracy = avg. 80% (pm10, pm25)
- multiple sensors test accuracy = avg. 96% (pm10, pm25)
  )
