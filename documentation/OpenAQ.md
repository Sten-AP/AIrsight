# OpenAQ Documentation

## What is OpenAQ?

OpenAQ is a provider of an open-source data platform which focuses on providing its users with air quality data.
They gather and expose this data through the use of sensors on the ground which semi-continuously measure the quality of the air surrounding it.
This data takes the form of measurements of specific particles or substances, like measuring the ppm of particulate matter under a certain size, like 10 micrometers.

It is largely thanks to the data from OpenAQ that we are able to train our Machine Learning model.

## What does our OpenAQ script do?

What our script does is quite simple.
Running our OpenAQ script does the following:

1. We call the OpenAQ API to retrieve sensor data
2. We pull the interesting datapoints out of each sensor and append the latest observation data to a json file
3. We post the json file with the sensor data to our own api, which then stores the data into our Influx DB
4. This script then repeats every half hour, to get a continuous stream of sensor data, visible in our frontend

The main purpose of this script is to essentially copy over some data from the actual OpenAQ API.
We focus down on sensors in Belgium specifically to keep the scope of our current project fairly limited.
This would be easily expanded upon to include multiple countries, however.

### Code repository

To go to the actual script itself in its backend project folder, click [here](../backend/OpenAQ)