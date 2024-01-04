def query_settings(lat, lon, start_date, end_date):
	box = 0.05

	query =  {
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
			"start": f"{start_date}",
			"end": f"{end_date}"
			}
		],
		"multiStringSelectValues": [
			{
			"name": "model",
			"value": [
				"chimere"
			]
			},
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
			"name": "type",
			"value": [
				"analysis"
			]
			},
			{
			"name": "level",
			"value": [
				"0"
			]
			},
			{
			"name": "leadtime_hour",
			"value": [
				"0"
			]
			},
			{
			"name": "time",
			"value": [
				"13:00"
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