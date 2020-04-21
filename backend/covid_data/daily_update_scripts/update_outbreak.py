import os
import requests
from datetime import datetime
from datetime import date
from covid_data.models import State, StateOutbreak, StateOutbreakCumulative
from covid_data.models import County, CountyOutbreak, CountyOutbreakCumulative
from covid_data.utilities import get_datetime_from_str, api_request_from_str

# Gets all state outbreak data and returns it as json object
def get_outbreak_data_by_state(outbreak_state):
    outbreak_str = "https://covidtracking.com/api/states/daily?state=" + outbreak_state.code
    return api_request_from_str(outbreak_str)

# Gets a all outbreak data for a specific state on a specified date and returns it as a json object
def get_outbreak_data_by_state_and_date(outbreak_state, outbreak_date):
    outbreak_str = "https://covidtracking.com/api/states/daily?state=" + outbreak_state.code + "&date=" + str(outbreak_date).replace("-","")
    return api_request_from_str(outbreak_str)

def update_state_outbreak(outbreak_json):
    record_date = get_datetime_from_str(str(outbreak_json['date']))
    record_state = State.objects.get(code=outbreak_json['state'])
            
    daily_cases = outbreak_json['positiveIncrease']
    daily_negative_tests = outbreak_json['negativeIncrease']
    daily_total_tested = outbreak_json['totalTestResultsIncrease']
    daily_deaths = outbreak_json['deathIncrease']
    
    try:
        daily_admitted_to_hospital = outbreak_json['hospitalizedIncrease']
    except:
        daily_admitted_to_hospital = None
    
    try:
        daily_hospitalized = outbreak_json['hospitalizedCurrently']
    except:
        daily_hospitalized = None
    
    try:
        daily_in_icu = outbreak_json['inIcuCurrently']
    except:
        daily_in_icu = None

    state_outbreak = StateOutbreak.objects.create(state = record_state, date=record_date, cases=daily_cases, negative_tests=daily_negative_tests, total_tested=daily_total_tested, deaths=daily_deaths, admitted_to_hospital=daily_admitted_to_hospital, hospitalized=daily_hospitalized, in_icu=daily_in_icu)
    state_outbreak.save()

    cumulative_cases = outbreak_json['positive']

    cumulative_negative_tests = outbreak_json['negative']

    print(cumulative_negative_tests)

    cumulative_total_tested = outbreak_json['totalTestResults']
    
    try:
        cumulative_deaths = outbreak_json['death']
    except:
        cumulative_deaths = None
    
    try:
        cumulative_hospitalized = outbreak_json['hospitalizedCumulative']
    except:
        cumulative_hospitalized = None
    
    try:
        cumulative_in_icu = outbreak_json['inIcuCumulative']
    except:
        cumulative_in_icu = None
    
    state_outbreak_cumulative = StateOutbreakCumulative.objects.create(state = record_state, date=record_date, cases=cumulative_cases, negative_tests=cumulative_negative_tests, total_tested=cumulative_total_tested, deaths=cumulative_deaths, hospitalized=cumulative_hospitalized, in_icu=cumulative_in_icu)
    state_outbreak_cumulative.save()
    

def update_all_state_outbreaks(date_to_update):
    states = State.objects.all()
    for state in states:
        outbreak_json = get_outbreak_data_by_state_and_date(state, date_to_update)
        update_state_outbreak(outbreak_json)
    
# Future release
def update_county_outbreak(county_to_update, date_to_update):
    pass

