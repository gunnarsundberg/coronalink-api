import os
from covid_data.models import State, County, CountyWeatherStation, CountyDailyWeather
from covid_data.utilities import api_request_from_str

# create weather station for each county
def create_county_weather_station(county):
    lat = county.latitude
    lon = county.longitude
    request_url = "https://api.meteostat.net/v1/stations/nearby?lat=" + str(lat) + "&lon=" + str(lon) + "&limit=1&key=" + os.environ['METEOSTAT_API_KEY']
    weather_station_json = api_request_from_str(request_url)['data'][0]
    station_id = weather_station_json['id']
    station_name = weather_station_json['name']
    new_station = CountyWeatherStation.objects.create(county=county, station_id=station_id, station_name=station_name)
    new_station.save()

def import_county_weather_stations():
    #for county in County.objects.all():
        #create_county_weather_station(county)
    pass