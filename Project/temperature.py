import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# read the cities.csv file
cities = pd.read_csv('cities.csv', header=None)

# get the coordinates in a list
lat = cities[2].tolist()
long = cities[3].tolist()

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
URL = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": lat,
	"longitude": long,
	"start_date": "2013-10-23",
	"end_date": "2023-11-06",
	"daily": "temperature_2m_mean"
}
responses = openmeteo.weather_api(URL, params=params)

print(responses[0].Daily().Variables(0).ValuesAsNumpy())

data = pd.DataFrame(columns = ['City', 'Country', 'Latitude', 'Longitude', 'Date', 'Temperature'])

data['City'] = cities[0]
data['Country'] = cities[1]
data['Date'] = pd.date_range(start = pd.to_date("2013-10-23"), end = pd.to_date("2023-10-23"), freq = 'D')
temp = []
lat = []
long = []
for i in range(len(responses)-1):
	tmp.append(responses[i].Daily().Variables(0).ValuesAsNumpy())
	lat.append(responses[i].Latitude())
	long.append(responses[i].Longitude())

data['Temperature'] = temp
data['Latitude'] = lat
data['Longitude'] = long

data.to_csv('temperature.csv', index=False)