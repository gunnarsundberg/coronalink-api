import os
import geopy.distance
from covid_data.models import State, County, DailyWeather
from covid_data.utilities import api_request_from_str

"""
This file is being kept in case our team needs to switch back to meteostat, but all functions are deprecated
"""

"""
# Create weather station for each county
def create_county_weather_station(county):
    lat = county.latitude
    lon = county.longitude
    request_url = "https://api.meteostat.net/v1/stations/nearby?lat=" + str(lat) + "&lon=" + str(lon) + "&limit=1&key=" + os.environ['METEOSTAT_API_KEY']
    try:
        weather_station_json = api_request_from_str(request_url)['data'][0]
        station_id = weather_station_json['id']
        station_name = weather_station_json['name']
        new_station = CountyWeatherStation.objects.create(county=county, station_id=station_id, station_name=station_name)
        new_station.save()
    except:
        print("Unable to get weather station for " + str(county.county_name) + " County, " + str(county.state.code))

# This function is a get function that merely gets the nearest station in the same state and returns it
def get_nearest_weather_station(county):
    county_coords = (county.latitude, county.longitude)
    # Variables for the nearest county distance and nearest county object
    distance_to_nearest_county = 9000
    nearest_county = None
    
    # Loop through all counties in the state and evaluate the distance between county arg and county being evaluated
    for county_eval in County.objects.filter(state=county.state):
        # We do not want to consider the county itself
        if county_eval.fips_code != county.fips_code:
            county_eval_cords = (county_eval.latitude, county_eval.longitude)
            county_eval_distance = geopy.distance.vincenty(county_coords, county_eval_cords).km
            # If distance is less than current minimum and the county has a weather station, set it as the new nearest county
            if county_eval_distance < distance_to_nearest_county and CountyWeatherStation.objects.filter(county=county_eval).exists():
                distance_to_nearest_county = county_eval_distance
                nearest_county = county_eval
    print(CountyWeatherStation.objects.get(county=nearest_county))
    return CountyWeatherStation.objects.get(county=nearest_county)

# For counties that don't have their own weather stations, use the nearest one. 
# This function loops through all counties in a state without a weather station, calls a get function, and creates a new county weather station model
# NOTE: This should be run for all counties without a weather station AFTER all counties in a state have been tried.
def use_nearest_weather_stations(state):
    for county in County.objects.filter(state=state):
        # If no weather station for the county exists, use the nearest one
        if not CountyWeatherStation.objects.filter(county=county).exists():
            nearest_weather_station = get_nearest_weather_station(county)
            new_station = CountyWeatherStation.objects.create(county=county, station_id=nearest_weather_station.station_id, station_name=nearest_weather_station.station_name)
            new_station.save()

def import_county_weather_stations():
    for state in State.objects.all():
        # Create weather stations for each county in the state
        for county in County.objects.filter(state=state):
            create_county_weather_station(county)
        # Use nearest weather station for counties in state with no weather station
        use_nearest_weather_stations(state)
"""