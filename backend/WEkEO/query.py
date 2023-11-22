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
        # "ensemble", # Enseble median
				# "chimere",  # INERIS (France)
        # "dehm",     # AARHUS UNIVERSITY (Denmark)
        # "emep",		  # MET Norway (Norway)
        # "euradim",  # Jülich IEK (Germany)
        # "gemaq",		# IEP-NRI (Poland)
        "lotos",		  # KNMI and TNO (Netherlands)
        # "match",		# SMHI (Sweden)
        # "minni",    # ENEA (Italy)
        # "mocage",		# METEO-FRANCE (France)
        # "monarch",	# BSC (Spain)
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
				"00:00",
				"01:00",
				"02:00",
				"03:00",
				"04:00",
				"05:00",
				"06:00",
				"07:00",
				"08:00",
				"09:00",
				"10:00",
				"11:00",
				"12:00",
				"13:00",
				"14:00",
				"15:00",
				"16:00",
				"17:00",
				"18:00",
				"19:00",
				"20:00",
				"21:00",
				"22:00",
				"23:00"
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