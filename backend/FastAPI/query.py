from datetime import datetime


def query_settings(lat, lon, start_date, end_date):
    date = datetime.now()
    hour = str(date.hour)
    if len(hour) == 1:
        hour = f"0{hour}"

    box = 0.05
    query = {
        "datasetId": "EO:ECMWF:DAT:CAMS_EUROPE_AIR_QUALITY_FORECASTS",
        "boundingBoxValues": [
            {
                "name": "area",
                "bbox": [
                        lon-box,
                        lat-box,
                        lon+box,
                        lat+box
                ]
            }
        ],
        "dateRangeSelectValues": [
            {
                "name": "date",
                "start": f"{start_date}T00:00:00.000Z",
                "end": f"{end_date}T00:00:00.000Z"
            }
        ],
        "multiStringSelectValues": [
            {
                "name": "variable",
                "value": [
                    "particulate_matter_10um",
                    "particulate_matter_2.5um",
                    "ozone",
                    "carbon_monoxide",
                    "nitrogen_dioxide",
                    "sulphur_dioxide"
                ]
            },
            {
                "name": "model",
                "value": [
                    # "ensemble",  # Enseble median
                    # "chimere",  # INERIS (France)
                    # "dehm",     # AARHUS UNIVERSITY (Denmark)
                    # "emep",		  # MET Norway (Norway)
                    # "euradim",  # Jülich IEK (Germany)
                    # "gemaq",		# IEP-NRI (Poland)
                    "lotos",		  # KNMI and TNO (Netherlands)
                    # "match",		# SMHI (Sweden)
                    # "minni",    # ENEA (Italy)
                    # "mocage",		# METEO-FRANCE (France)
                    # "monarch",  # BSC (Spain)
                    # "silam"			# FMI (Finland)
                ]
            },
            {
                "name": "level",
                "value": [
                        "0"
                ]
            },
            {
                "name": "type",
                "value": [
                        "analysis"
                ]
            },
            {
                "name": "time",
                "value": [
                    f"{hour}:00",
                ]
            },
            {
                "name": "leadtime_hour",
                "value": [
                        "0"
                ]
            }
        ],
        "stringChoiceValues": [
            {
                "name": "format",
                "value": "netcdf"
            }
        ]
    }
    return query
