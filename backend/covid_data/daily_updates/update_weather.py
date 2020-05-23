import os
import threading
from covid_data.utilities import api_request_from_str, get_local_timestamp, get_local_timezone
from covid_data.models import State, County, DailyWeather

# Get all weather data for county provided by OpenWeatherMap and return json
def get_county_weather_json(county, date_to_update):
    local_timezone = get_local_timezone(county.latitude, county.longitude)
    start_timestamp, end_timestamp = get_local_timestamp(local_timezone, date_to_update)
    
    url = "https://history.openweathermap.org/data/2.5/history/city?lat=" + str(county.latitude) + "&lon=" + str(county.longitude) + "&start=" + str(start_timestamp) + "&end=" + str(end_timestamp) + "&appid=" + str(os.environ['OPENWEATHERMAP_API_KEY'])
    
    return api_request_from_str(url)

# Get uv index for county provided by OpenWeatherMap and return value
def get_county_uv_index(county, date_to_update):
    local_timezone = get_local_timezone(county.latitude, county.longitude)
    start_timestamp, end_timestamp = get_local_timestamp(local_timezone, date_to_update)
    
    url = "https://api.openweathermap.org/data/2.5/uvi/history?lat=" + str(county.latitude) + "&lon=" + str(county.longitude) + "&start=" + str(start_timestamp) + "&end=" + str(end_timestamp) + "&appid=" + str(os.environ['OPENWEATHERMAP_API_KEY'])
    
    return api_request_from_str(url)[0]['value']

# update county weather records
def update_county_weather(county, date_to_update):
    
    county_weather_json = get_county_weather_json(county, date_to_update)
    
    # Initialize variables
    temp_sum = None
    humidity_sum = None
    max_temp = None
    min_temp = None
    uv_index = get_county_uv_index(county, date_to_update)

    for i in range(0, county_weather_json['cnt']):
        # Sum temperature values for each hour of the day.
        if temp_sum is not None:
            temp_sum += county_weather_json['list'][i]['main']['temp']
        else:
            temp_sum = county_weather_json['list'][i]['main']['temp']
        
        # Sum humidity values for each hour of the day
        if humidity_sum is not None:
            humidity_sum += county_weather_json['list'][i]['main']['humidity']
        else:
            humidity_sum = county_weather_json['list'][i]['main']['humidity']

        if max_temp is None or max_temp < county_weather_json['list'][i]['main']['temp_max']:
            max_temp = county_weather_json['list'][i]['main']['temp_max']

        if min_temp is None or min_temp > county_weather_json['list'][i]['main']['temp_min']:
            min_temp = county_weather_json['list'][i]['main']['temp_min']

    # Calculate average values from sums
    temp_avg = round(temp_sum /county_weather_json['cnt'], 2)
    humidity_avg = round(humidity_sum / county_weather_json['cnt'], 2)
      
    #Create county weather model
    daily_weather = DailyWeather.objects.create(region=county, date=date_to_update, avg_temperature=temp_avg, max_temperature=max_temp, min_temperature=min_temp, avg_humidity=humidity_avg, uv_index=uv_index)
    daily_weather.save()  

def update_state_weather(state, date_to_update):
    pass
    #TODO: Write entire state weather function