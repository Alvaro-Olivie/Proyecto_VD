import { fetchWeatherApi } from 'openmeteo';
	
const params = {
	"latitude": [52.52, 52.52],
	"longitude": [13.41, 13.41],
	"start_date": "2023-10-17",
	"end_date": "2023-10-31",
	"daily": "temperature_2m_mean"
};
const url = "https://archive-api.open-meteo.com/v1/archive";
const responses = await fetchWeatherApi(url, params);

// Helper function to form time ranges
const range = (start: number, stop: number, step: number) =>
	Array.from({ length: (stop - start) / step }, (_, i) => start + i * step);

// Process first location. Add a for-loop for multiple locations or weather models
const response = responses[0];

// Attributes for timezone and location
const utcOffsetSeconds = response.utcOffsetSeconds();
const timezone = response.timezone();
const timezoneAbbreviation = response.timezoneAbbreviation();
const latitude = response.latitude();
const longitude = response.longitude();

const daily = response.daily()!;

// Note: The order of weather variables in the URL query and the indices below need to match!
const weatherData = {

	daily: {
		time: range(Number(daily.time()), Number(daily.timeEnd()), daily.interval()).map(
			(t) => new Date((t + utcOffsetSeconds) * 1000)
		),
		temperature2mMean: daily.variables(0)!.valuesArray()!,
	},

};

// `weatherData` now contains a simple structure with arrays for datetime and weather data
for (let i = 0; i < weatherData.daily.time.length; i++) {
	console.log(
		weatherData.daily.time[i].toISOString(),
		weatherData.daily.temperature2mMean[i]
	);
}