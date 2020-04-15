import os
import requests
from datetime import datetime
from datetime import date
from datetime import time
from data_collection.models import State, StateOutbreak, StateOutbreakCumulative
from data_collection.models import County, CountyOutbreak, CountyOutbreakCumulative

# Gets all state outbreak data and returns it as json object
def get_outbreak_data_by_state(outbreak_state):
    for i in range(4):
        try:
            new_outbreak_data = requests.get("https://covidtracking.com/api/states/daily?state=" + outbreak_state.code)
            return new_outbreak_data.json()
        except:
            print("Unable to get data. Retrying..")

# Gets a all outbreak data for a specific state on a specified date and returns it as a json object
def get_outbreak_data_by_state_and_date(outbreak_state, outbreak_date):
    for i in range(4):
        try:
            new_outbreak_data = requests.get("https://covidtracking.com/api/states/daily?state=" + outbreak_state.code + "&date=" + str(outbreak_date).replace("-",""))
            return new_outbreak_data.json()
        except:
            print("Unable to get data. Retrying..")


def get_datetime(datetime_str):
    year = datetime_str[:4]
    month = datetime_str[4:6]
    day = datetime_str[6:8]
    return datetime(year=year, month=month, day=day)

def update_state_outbreak(outbreak_json):
        for outbreak_record in outbreak_json:
            daily_cases = outbreak_record['positiveIncrease']
            daily_negative_tests = outbreak_record['negativeIncrease']
            daily_total_tested = outbreak_record['totalTestResultsIncrease']
            daily_deaths = outbreak_record['deathIncrease']
            daily_admitted_to_hospital = outbreak_record['hospitalizedIncrease']
            daily_hospitalized = outbreak_record['hospitalized']
            record_date = get_datetime(outbreak_record['date'])
            state_outbreak = StateOutbreak.objects.create(state = state_to_update, cases=daily_cases, negative_tests=daily_negative_tests, total_tested=daily_total_tested, deaths=daily_deaths, admitted_to_hospital=daily_admitted_to_hospital, hospitalized=daily_hospitalized)
            state_outbreak.save()

            cumulative_cases = outbreak_record['positive']
            cumulative_negative_tests = outbreak_record['negative']
            cumulative_total_tested = outbreak_record['totalTestResults']
            cumulative_deaths = outbreak_record['death']
            cumulative_hospitalized = outbreak_record['hospitalizedCumulative']
            state_outbreak_cumulative = StateOutbreakCumulative.objects.create(state = state_to_update)
            state_outbreak_cumulative.save()
    

def update_all_state_outbreaks(date_to_update):
    states = State.objects.all()
    for state in states:
        outbreak_json = get_outbreak_data_by_state_and_date(state, date_to_update)
        update_state_outbreak(outbreak_json)
    

def update_county_outbreak(county_to_update, date_to_update):
    pass

