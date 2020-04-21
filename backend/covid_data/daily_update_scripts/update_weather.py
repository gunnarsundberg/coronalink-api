import os
from covid_data.utilities import api_request_from_str
from covid_data.models import State, County, CountyWeatherStation, CountyDailyWeather

# get weather for county
def get_county_weather(county, date_to_update):
    county_station = CountyWeatherStation.objects.get(county=county)
    request_url = "https://api.meteostat.net/v1/history/daily?station=" + county_station + "&start=" + str(date_to_update) + "&end=" + str(date_to_update) + "&key=" + os.environ['METEOSTAT_API_KEY']
    weather_json = api_request_from_str(request_url)['data'][0]
    #return weather_json['']

def get_county_uv_index(county, date_to_update):
    pass

# update county weather records
def update_county_weather(county, date_to_update):
    pass

def update_state_weather(state, date_to_update):
    pass