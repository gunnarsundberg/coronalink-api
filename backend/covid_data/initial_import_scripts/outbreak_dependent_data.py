import datetime
import requests
import threading
from covid_data.models import State, County, StateOutbreakCumulative, StateOutbreak
from covid_data.daily_update_scripts.update_outbreak import update_state_outbreak, get_outbreak_data_by_state
from covid_data.daily_update_scripts.update_flights import update_state_flights
from covid_data.daily_update_scripts.update_weather import update_county_weather
from covid_data.utilities import get_datetime_from_str

import time as t

def import_outbreak_dependent_data():
    states = State.objects.all()
    print("Importing outbreak related data for all states...")
    for i, state in enumerate(states):
        print("Working on " + state.state_name + " (" + str(i+1) + "/" + str(states.count()) + ")")
        t.sleep(1)
        outbreak_json = get_outbreak_data_by_state(state)
        for outbreak_record in outbreak_json:
            if int(outbreak_record['positive']) > 99:
                date_to_update = get_datetime_from_str(str(outbreak_record['date']))

                print("Importing outbreak data for " + state.state_name)
                update_state_outbreak(outbreak_record)

                print("Importing flight data for " + state.state_name)
                #update_state_flights(state, date_to_update)
                #threading.Thread(target = update_state_flights, args = (state, date_to_update)).start()
                
                state_counties = County.objects.filter(state=state)
                
                print("Importing county weather data for " + state.state_name)
                for county in state_counties:
                    update_county_weather(county, date_to_update)
    