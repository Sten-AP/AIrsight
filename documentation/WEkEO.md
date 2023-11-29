# WEkEO Documentation

## What is WEkEO?

WEkEO is one of the European DIAS (Data and Information Access services), which allows a centralised access to all Copernicus data and large computations on a cloud infrastructure.

It is an online cloud platform that collates and presents sattelite data with a focus on environmental aspects. 
It's possible to request a wide variety of satellite data through their cloud infrastructure using Jupyter Notebooks, but this isn't as easy for every layperson.

This is why we are developing our own cloud platform that utilizes data from, among other sources, WEkEO, to present their data in a slightly more user-friendly manner.

## What does our WEkEO script do?

Running the WEkEO script does the following:

1. Calls our own API to retrieve location data on each of the OpenAQ ground sensors.
2. Uses this location data to call the WEkEO API and retrieve satellite data surrounding every individual ground sensor.  
3. Save and write the data from the WEkEO API to the database, using the same id as the sensor of which the location data was used.

This script doesn't run amazingly fast, since we do an expensive API call that returns a lot of data, of which we use a set amount of datapoints to continue with.  
It does, however, provide us with complete and valuable data to later use in any frontend applications. All in combination with the ground sensor data from OpenAQ.
