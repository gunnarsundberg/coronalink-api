from django.conf import settings
from datetime import date
from tqdm import tqdm
import pandas as pd
from timezonefinder import TimezoneFinder
from covid_data.models import State, County, RegionAdjacency

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

# Function to convert   
def listToString(s: list):  
    
    # initialize an empty string 
    str1 = "" 
    
    # return string   
    return (str1.join(s)) 

def create_adjacency_record(county_fips, adjacent_counties):
    
    if county_fips:
        county = County.objects.get(fips_code=county_fips)
        for adjacent_fips in adjacent_counties:
            adjacent_county = County.objects.get(fips_code=adjacent_fips)
            new_adjacency = RegionAdjacency.objects.create(region=county, adjacent_region=adjacent_county)
            new_adjacency.save()
            

def import_county_adjacencies():       
    with open(settings.BASE_DIR + "/covid_data/initial_imports/data/county_adjacency.txt") as county_file:
        adjacent_counties = []
        current_county_fips = ""
        for line in county_file:
            if line.startswith("\""):
                create_adjacency_record(current_county_fips, adjacent_counties)
                adjacent_counties = []
                line_digits_list = list(filter(str.isdigit, line))
                line_digits = listToString(line_digits_list)
                current_county_fips = line_digits[:5]
                
                adjacent_counties.append(line_digits[5:])

            else:
                line_digits_list = list(filter(str.isdigit, line))
                line_digits = listToString(line_digits_list)
                if (line_digits != current_county_fips):
                    adjacent_counties.append(line_digits)
        # Create record for last county in file
        create_adjacency_record(current_county_fips, adjacent_counties)

def import_edge_weights():
    commute_flow = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/commute_flow.csv", dtype={'res_county_fips': 'object', 'res_state_fips': 'object', 'work_county_fips': 'object', 'work_state_fips': 'object'})
    for index, row in commute_flow.iterrows():
        # Try getting County records. If they don't exist, continue
        try:
            res_state_fips = str(row['res_state_fips'])
            work_state_fips = str(row['work_state_fips'])

            county_fips = res_state_fips + str(row['res_county_fips'])
            adjacent_fips = work_state_fips + str(row['work_county_fips'])

            county = County.objects.get(fips_code=county_fips)
            adjacent_county = County.objects.get(fips_code=adjacent_fips)
        except:
            continue

        # We will only track commuter flow for adjacent counties
        if RegionAdjacency.objects.filter(region=county).filter(adjacent_region=adjacent_county).exists():
            adjacency_record = RegionAdjacency.objects.filter(region=county).get(adjacent_region=adjacent_county)
            adjacency_record.edge_weight = row['number_of_workers']
            adjacency_record.save()