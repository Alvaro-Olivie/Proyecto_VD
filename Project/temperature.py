import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from cities import get_cities


def get_temperatures(cityFilter, dates):
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# read the cities.csv file
	city = get_cities()

	# filter the city list with the city names in the filter list
	if filter is not None:
		city = city[city[0].isin(cityFilter)]

	# get the coordinates in a list
	lat = city[2].tolist()
	long = city[3].tolist()

	print(dates)
	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	URL = "https://archive-api.open-meteo.com/v1/archive"
	params = {
		"latitude": lat,
		"longitude": long,
		"start_date": dates[0],
		"end_date": dates[1],
		"daily": "temperature_2m_mean"
	}
	responses = openmeteo.weather_api(URL, params=params)

	data = pd.DataFrame(columns = ['City', 'Country', 'Latitude', 'Longitude', 'Date', 'Temperature'])

	dfs = []

	c = city[0].tolist()

	for j in range(len(c)):
		df = pd.DataFrame(columns = ['City', 'Date', 'Temperature'])
		
		df['Temperature'] = responses[j].Daily().Variables(0).ValuesAsNumpy()

		df['Date'] = pd.date_range(start = pd.to_datetime(dates[0]), periods = len(df), freq = 'D')
		df['City'] = [c[j]]*len(df)

		dfs.append(df)
	
	data = pd.concat(dfs)

	df_pivot = data.pivot(index='Date', columns='City', values='Temperature')

	return df_pivot
