from django.conf import settings
import pandas as pd
from datetime import date as d 
from datetime import timedelta
from covid_data.tasks import create_periodic_tasks
# Import scripts for non-outbreak-dependent data. This will be recorded regardless of outbreak date
from covid_data.initial_imports.regions import import_states, import_counties, import_county_adjacencies
from covid_data.initial_imports.airports import import_state_airports
from covid_data.initial_imports.demographics import import_county_demographics, import_state_demographics
from covid_data.initial_imports.healthcare import import_state_healthcare
from covid_data.daily_updates.update_outbreak import update_state_outbreak, update_county_outbreak
from covid_data.daily_updates.update_weather import update_state_weather

# Models
from covid_data.models import State, Outbreak, OutbreakCumulative, DisplayDate

# Import outbreak-dependent data. This will only be recorded when cases exceed 100
from covid_data.initial_imports.outbreak_related_data import import_outbreak_related_data

from covid_data.models import State
from django.core.management.base import BaseCommand

import time

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        start_time = time.time()

        # Get CSV data
        states = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/states_final.csv", dtype={'fips': 'str'})
        counties = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/counties.csv", dtype={'FIPS': 'str'})
        state_airports = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/airports_usa.csv")

        counties['Land Areakm'].replace(',','', regex=True, inplace=True)
        counties['Land Areakm'] = counties['Land Areakm'].apply(pd.to_numeric,errors='coerce')

        today = d.today()

        display_date = DisplayDate.objects.create(date=today-timedelta(days=1))
        display_date.save()

        # Import regions
        import_states(states)
        import_counties(counties)

        print("Importing county adjacencies...")
        import_county_adjacencies()

        # Import airports
        print("Importing airports...")
        import_state_airports(state_airports)

        # Import healthcare information
        print("Importing healthcare information...")
        import_state_healthcare()

        # Import outbreak data 
        print("Importing state outbreak data...")
        update_state_outbreak()

        print("Importing county outbreak data...")
        update_county_outbreak()

        # Fix any wrong calculations for outbreak dates caused by import order (see logic in save method)
        print("Verifying outbreak dates...")
        for outbreak in Outbreak.objects.all():
            outbreak.save()
        print("Verifying cumulative outbreak dates...")
        for outbreak in OutbreakCumulative.objects.all():
            outbreak.save()

        create_periodic_tasks()

        # Imports all daily data for outbreak days
        import_outbreak_related_data(State.objects.all())

        # Import demographics
        import_county_demographics()
        import_state_demographics()

        for outbreak in Outbreak.objects.filter(region__in=State.objects.all()):
            date = outbreak.date
            state = outbreak.region.state
            update_state_weather(state, date)

        print("--- %s minutes ---" % ((time.time() - start_time)/60))