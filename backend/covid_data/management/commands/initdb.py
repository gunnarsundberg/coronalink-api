from django.conf import settings
import io

import requests
import pandas as pd
from datetime import date, timedelta
# Import scripts for non-outbreak-dependent data. This will be recorded regardless of outbreak date
from covid_data.initial_imports.regions import import_states, import_counties
from covid_data.initial_imports.airports import import_state_airports
from covid_data.initial_imports.school_closures import import_state_school_closures
from covid_data.initial_imports.stay_in_place import import_state_stay_in_place
from covid_data.initial_imports.demographics import import_county_demographics, import_state_demographics
from covid_data.initial_imports.healthcare import import_state_healthcare
from covid_data.daily_updates.update_outbreak import update_state_outbreak

# Models
from covid_data.models import Outbreak, OutbreakCumulative

# Import outbreak-dependent data. This will only be recorded when cases exceed 100
from covid_data.initial_imports.outbreak_dependent_data import import_outbreak_dependent_data

from covid_data.models import State
from django.core.management.base import BaseCommand

import time

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        # Get CSV data
        start_time = time.time()

        state_outbreak_csv_url = "https://raw.githubusercontent.com/COVID19Tracking/covid-tracking-data/master/data/states_daily_4pm_et.csv"
        state_outbreak_csv = requests.get(state_outbreak_csv_url).content

        states = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/states_final.csv", dtype={'fips': 'str'})
        counties = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/counties.csv", dtype={'FIPS': 'str'})
        state_airports = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/airports_usa.csv")
        state_school_closures = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/school_closure_order.csv")
        state_stay_in_place = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/stay_in_place_order.csv")
        state_outbreak_data = pd.read_csv(io.StringIO(state_outbreak_csv.decode('utf-8')))

        counties['Land Areakm'].replace(',','', regex=True, inplace=True)
        counties['Land Areakm'] = counties['Land Areakm'].apply(pd.to_numeric,errors='coerce')

        # Import regions
        import_states(states)
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

        # Import demographics
        import_county_demographics()
        import_state_demographics()

        # Import healthcare information
        print("Importing healthcare information...")
        import_state_healthcare()

        # Import outbreak data 
        print("Importing state outbreak data...")
        update_state_outbreak(state_outbreak_data)

        # Fix any wrong calculations for outbreak dates caused by import order (see logic in save method)
        print("Verifying outbreak dates...")
        for outbreak in Outbreak.objects.all():
            outbreak.save()

        # Imports all daily data for outbreak days
        import_outbreak_dependent_data(State.objects.all())

        yesterday = date.today() - timedelta(days=1)

        print("--- %s minutes ---" % ((time.time() - start_time)/60))