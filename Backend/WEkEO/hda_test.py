from hda import Client, Configuration

hda_client = Client()

lat = 51.3
lon = 4.42

box = 0.01

bbox = [
    lon-box,
    lat-box,
    lon+box,
    lat+box
]

data = {
    "datasetId": "EO:ECMWF:DAT:CAMS_EUROPE_AIR_QUALITY_FORECASTS",
    "boundingBoxValues": [
        {
            "name": "area",
            "bbox": bbox
        }
    ],
    "dateRangeSelectValues": [
        {
            "name": "date",
            "start": "2020-10-10T00:00:00.000Z",
            "end": "2023-10-11T23:59:59.999Z"
        }
    ],
    "multiStringSelectValues": [
        {
            "name": "level",
            "value": [
                "0",
            ]
        },
        {
            "name": "model",
            "value": [
                "ensemble"
            ]
        },
        {
            "name": "variable",
            "value": [
                "particulate_matter_10um",
                "particulate_matter_2.5um"
            ]
        },
        {
            "name": "type",
            "value": [
                "forecast"
            ]
        },
        {
            "name": "time",
            "value": [
                "00:00"
            ]
        },
        {
            "name": "leadtime_hour",
            'value': ['0',
                      '6',
                      '12',
                      '18',
                      '24',
                      '30',
                      '36',
                      '42',
                      '48',
                      '54',
                      '60',
                      '66',
                      '72']
        }
    ],
    "stringChoiceValues": [
        {
            "name": "format",
            "value": "netcdf"
        }
    ]
}

matches = hda_client.search(data)
print(matches)

matches.download('./data/')
