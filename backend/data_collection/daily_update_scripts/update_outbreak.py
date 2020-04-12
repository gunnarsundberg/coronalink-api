import os
import requests
from datetime import datetime
from datetime import date
from datetime import time
from data_collection.models import State, StateOutbreak, StateOutbreakCumulative
from data_collection.models import County, CountyOutbreak, CountyOutbreakCumulative


def update_state_outbreak(state_to_update, date_to_update):
    state_outbreak = StateOutbreak.objects.get(state = state_to_update)
    #state_outbreak_cumulative = StateOutbreakCumulative.objects.filter(state = state_to_update)
    
    new_outbreak_data = requests.get("https://covidtracking.com/api/states/daily?state=" + state_to_update.code + "&date=" + str(date_to_update).replace("-",""))
    
    try:
        state_outbreak.cases = new_outbreak_data.json()['positiveIncrease']
        state_outbreak.negative_tests = new_outbreak_data.json()['negativeIncrease']
        state_outbreak.total_tested = new_outbreak_data.json()['totalTestResultsIncrease']
        state_outbreak.deaths = new_outbreak_data.json()['deathIncrease']
        state_outbreak.hospitalized = new_outbreak_data.json()['hospitalizedIncrease']
        state_outbreak.save()

        #state_outbreak_cumulative.cases = new_outbreak_data.json()['positive']
        #state_outbreak_cumulative.negative_tests = new_outbreak_data.json()['negative']
        #state_outbreak_cumulative.total_tested_increase = new_outbreak_data.json()['totalTestResults']
        #state_outbreak_cumulative.deaths = new_outbreak_data.json()['death']
        #state_outbreak_cumulative.hospitalized = new_outbreak_data.json()['hospitalizedCumulative']
        #state_outbreak_cumulative.save()
    except:
        print("Data for this date is not available!")

def update_county_outbreak(county_to_update, date_to_update):
    pass

#def update_outbreak(date_to_update):
