from datetime import date
from timezonefinder import TimezoneFinder
from covid_data.models import State, County

# Takes in pandas dataframe and adds states
def import_states(states):
    for index, row in states.iterrows():
        state_name = row['State']
        state_code = row['Code']
        state_fips = row['fips']
        new_state = State(state_name=state_name, code=state_code, fips_code=state_fips)
        new_state.save()  

# Takes in pandas dataframe and adds counties
def import_counties(counties):
    for index, row in counties.iterrows():
        tf = TimezoneFinder()
        county_state_code = row['State']
        county_name = row['County']
        county_fips = row['FIPS']
        county_latitude_str = str(row['Latitude'])
        county_latitude = float(county_latitude_str)
        county_longitude_str = str(row['Longitude'])
        county_longitude = float(county_longitude_str)
        county_timezone_str = tf.timezone_at(lat=county_latitude, lng=county_longitude)
        county_state = State.objects.get(code=county_state_code)
        new_county = County(state=county_state, county_name=county_name, fips_code=county_fips, latitude=county_latitude, longitude=county_longitude, timezone_str=county_timezone_str)
        new_county.save()