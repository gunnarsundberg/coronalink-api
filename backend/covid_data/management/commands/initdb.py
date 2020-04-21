from django.conf import settings
import pandas as pd
from datetime import date, timedelta
# Import scripts for non-outbreak-dependent data. This will be recorded regardless of outbreak date
from covid_data.initial_import_scripts.regions import import_states, import_counties
from covid_data.initial_import_scripts.airports import import_state_airports
from covid_data.initial_import_scripts.school_closures import import_state_school_closures
from covid_data.initial_import_scripts.stay_in_place import import_state_stay_in_place
from covid_data.initial_import_scripts.weather import import_county_weather_stations
from covid_data.initial_import_scripts.demographics import import_county_demographics, import_state_demographics
from covid_data.initial_import_scripts.healthcare import import_state_healthcare

# Import outbreak-dependent data. This will only be recorded when cases exceed 100
from covid_data.initial_import_scripts.outbreak_dependent_data import import_outbreak_dependent_data

from covid_data.models import State
from django.core.management.base import BaseCommand

import time

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        # Get CSV data
        start_time = time.time()

        states = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_import_scripts/data/states_final.csv")
        counties = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_import_scripts/data/counties.csv")
        state_airports = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_import_scripts/data/airports_usa.csv")
        state_school_closures = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_import_scripts/data/school_closure_order.csv")
        state_stay_in_place = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_import_scripts/data/stay_in_place_order.csv")
        
        #yesterday = date.today() - timedelta(days=1)

        # Import regions
        print("Importing states...")
        import_states(states)
        print("Importing counties...")
        import_counties(counties)

        # Import airports
        print("Importing airports...")
        import_state_airports(state_airports)

        # Import school closures
        print("Importing school closures...")
        import_state_school_closures(state_school_closures)

        # Import stay-in-place
        print("Importing stay in place orders...")
        import_state_stay_in_place(state_stay_in_place)

        # Import weather stations
        print("Importing weather stations...")
        import_county_weather_stations()

        # Import demographics
        print("Importing county demographics...")
        import_county_demographics()
        print("Importing state demographics...")
        import_state_demographics()

        # Import healthcare information
        print("Importing healthcare information...")
        import_state_healthcare()

        # Imports all daily data for outbreak days
        import_outbreak_dependent_data()

        print("--- %s minutes ---" % ((time.time() - start_time)/60))