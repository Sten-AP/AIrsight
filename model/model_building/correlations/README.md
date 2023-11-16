# Correlations between variables

In this readme we'll go over the different kinds of variables (from wekeo) and which ones have a strong correlation with eachother.

It'll give us a better idea on how to form a dataset and which variables to seperate and which to combine.

## The different types of variables

- time
- pm10 (Particulate Matter)
- pm25(pm2.5)
- no2 (Nitrogen Dioxide)
- o3 (Ozone)
- so2 (Sulphur Dioxide)
- co (Carbon Monoxide)
- nmvoc (Non-methane Volatile Organic Compounds)
- no (Nitrogen monoxide)

## correlation output

|         |   time    |   pm10    |   pm25    |    no2    |    o3     |    so2    |  co_conc  |   nmvoc   |    no     |
| ------- | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| time    | 1.000000  | -0.066382 | -0.223503 | -0.186519 | 0.451475  | -0.182320 | -0.269970 | -0.205288 | -0.242711 |
| pm10    | -0.066382 | 1.000000  | 0.923521  | 0.468826  | 0.002167  | 0.417225  | 0.334121  | 0.339140  | 0.189866  |
| pm25    | -0.223503 | 0.923521  | 1.000000  | 0.643713  | -0.238136 | 0.521706  | 0.530841  | 0.542704  | 0.331656  |
| no2     | -0.186519 | 0.468826  | 0.643713  | 1.000000  | -0.664725 | 0.667095  | 0.705985  | 0.786376  | 0.494981  |
| o3      | 0.451475  | 0.002167  | -0.238136 | -0.664725 | 1.000000  | -0.301014 | -0.471999 | -0.650932 | -0.419938 |
| so2     | -0.182320 | 0.417225  | 0.521706  | 0.667095  | -0.301014 | 1.000000  | 0.790719  | 0.624516  | 0.808789  |
| co_conc | -0.269970 | 0.334121  | 0.530841  | 0.705985  | -0.471999 | 0.790719  | 1.000000  | 0.774434  | 0.722463  |
| nmvoc   | -0.205288 | 0.339140  | 0.542704  | 0.786376  | -0.650932 | 0.624516  | 0.774434  | 1.000000  | 0.733941  |
| no      | -0.242711 | 0.189866  | 0.331656  | 0.494981  | -0.419938 | 0.808789  | 0.722463  | 0.733941  | 1.000000  |

## best combinations for datasets

**pm10**: pm25, no2, so2, co_conc, nmvoc, and no == high positive correlations

**pm25**: pm10, no2, so2, co_conc, nmvoc, and no == high positive correlations

**no2**: pm25, so2, co_conc, nmvoc, and no == high postitive correlations

**o3**: time == only postive correlation

**so2**: no2, co_conc, nmvoc, and no == high positive correlations

**co**: pm25, no2, so2, nmvoc, and no == high positive correlations

**nmvoc**: pm25, no2, so2, co_conc, and no == high positive correlation.

**no**: pm25, no2, so2, co_conc, and nmvoc == high positive correlation

## Remarks
NO seems to heavily lower test results for the models, I suggest just leaving it off.