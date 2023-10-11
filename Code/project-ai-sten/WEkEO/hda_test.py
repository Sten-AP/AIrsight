from pathlib import Path
from hda import Client, Configuration
import json
import time


hdarc = Path(Path.home() / '.hdarc')

if not hdarc.is_file():
    import getpass
    USERNAME = input('Enter your username: ')
    PASSWORD = getpass.getpass('Enter your password: ')

    with open(Path.home() / '.hdarc', 'w') as f:
        f.write(f'user:{USERNAME}\n')
        f.write(f'password:{PASSWORD}\n')

hda_client = Client()

lat = 51.3
lon = 4.42

bbox = [
    lon-0.01,
    lat-0.01,
    lon+0.01,
    lat+0.01
]


data = {
    "datasetId": "EO:ECMWF:DAT:CAMS_EUROPE_AIR_QUALITY_FORECASTS",
    "boundingBoxValues": [{"name": "area", "bbox": bbox}],
    "dateRangeSelectValues": [{"name": "date", "start": "2021-02-04T00:00:00.000Z", "end": "2021-02-04T00:00:00.000Z"}],
    "multiStringSelectValues": [
        {"name": "model", "value": ["ensemble"]},
        {"name": "variable", "value": ["nitrogen_dioxide"]},
        {"name": "type", "value": ["forecast"]},
        {"name": "level", "value": ["0"]},
        {"name": "leadtime_hour", "value": [
            "0", "6", "12", "18", "24", "30", "36", "42", "48", "54", "60", "66", "72"]},
        {"name": "time", "value": ["00:00"]}
    ],
    "stringChoiceValues": [{"name": "format", "value": "netcdf"}]
}


matches = hda_client.search(json.dumps(data))
print(matches)

matches.download('./data/')
