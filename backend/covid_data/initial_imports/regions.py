from datetime import date
from tqdm import tqdm
from timezonefinder import TimezoneFinder
from covid_data.models import State, County

# Takes in pandas dataframe and adds states
def import_states(states):
    progress_bar = tqdm(desc="Importing States", total=len(states.index))
    for index, row in states.iterrows():
        state_name = row['State']
        state_code = row['Code']
        state_fips = row['fips']
        land_area = row['land_area']
        
        new_state = State(name=state_name, code=state_code, fips_code=state_fips, land_area=land_area)
        new_state.save()
        
        progress_bar.update(1) 

# Takes in pandas dataframe and adds counties
def import_counties(counties):
    tf = TimezoneFinder()
    
    progress_bar = tqdm(desc="Importing Counties", total=len(counties.index))
    for index, row in counties.iterrows():
        county_state_code = row['State']
        county_name = row['County']
        county_fips = row['FIPS']
        county_land_area = row['Land Areakm']
        county_latitude_str = str(row['Latitude'])
        county_latitude = float(county_latitude_str)
        county_longitude_str = str(row['Longitude'])
        county_longitude = float(county_longitude_str)
        county_timezone_str = tf.timezone_at(lat=county_latitude, lng=county_longitude)
        county_state = State.objects.get(code=county_state_code)
        
        new_county = County(parent_region=county_state, name=county_name, fips_code=county_fips, latitude=county_latitude, longitude=county_longitude, timezone_str=county_timezone_str, land_area=county_land_area)
        new_county.save()
        
        progress_bar.update(1)