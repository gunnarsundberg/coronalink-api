import pandas as pd
from datetime import date
from data_collection.models import State, County, StateAirport, StateSchoolClosure, StateStayInPlace

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
        county_state_code = row['State']
        county_name = row['County']
        county_fips = row['FIPS']
        county_latitude_str = str(row['Latitude'])
        county_latitude = float(county_latitude_str)
        county_longitude_str = str(row['Longitude'])
        county_longitude = float(county_longitude_str)
        county_state = State.objects.get(code=county_state_code)
        new_county = County(state=county_state, county_name=county_name, fips_code=county_fips, latitude=county_latitude, longitude=county_longitude)
        new_county.save()

# Takes in pandas dataframe and adds counties
def import_state_airports(airports):
    for index, row in airports.iterrows():
        airport_name = row['name']
        airport_icao_code = row['icao']
        airport_timezone = row['timezone_pytz']
        airport_state_name = row['state']
        airport_state_object = State.objects.get(state_name=airport_state_name)

        new_state_airport = StateAirport(airport_name=airport_name, icao_code=airport_icao_code, timezone=airport_timezone, state=airport_state_object)
        new_state_airport.save()

# Takes in pandas dataframe and adds state school closures
def import_state_school_closures(school_closure):
    for index, row in school_closure.iterrows():
        school_state_str = str(row['State'])
        print(school_state_str)
        school_closure_bool = (row['Instated'] == 1)
        school_date_of_order = row['Date of Order']
        school_state_object = State.objects.get(state_name=school_state_str)

        new_state_school_closure = StateSchoolClosure(order=school_closure_bool, date=school_date_of_order, state=school_state_object)
        new_state_school_closure.save()

def import_state_stay_in_place(stay_in_place):
    for index, row in stay_in_place.iterrows():
        stay_in_place_state_str = str(row['State'])
        stay_in_place_bool = (row['Instated'] == 1)
        stay_in_place_date_of_order = row['Date of Order']
        stay_in_place_state_object = State.objects.get(state_name=stay_in_place_state_str)

        new_state_stay_in_place = StateStayInPlace(order=stay_in_place_bool, date=stay_in_place_date_of_order, state=stay_in_place_state_object)
        new_state_stay_in_place.save()