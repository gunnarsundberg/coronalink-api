from django.conf import settings
import pandas as pd
from data_collection.initial_import_scripts.import_from_csv import import_states, import_counties, import_state_airports, import_state_school_closures, import_state_stay_in_place
from data_collection.models import State
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        states = pd.read_csv(settings.BASE_DIR + "/data_collection/initial_import_scripts/data/states_final.csv")
        counties = pd.read_csv(settings.BASE_DIR + "/data_collection/initial_import_scripts/data/counties.csv")
        state_airports = pd.read_csv(settings.BASE_DIR + "/data_collection/initial_import_scripts/data/airports_usa.csv")
        state_school_closures = pd.read_csv(settings.BASE_DIR + "/data_collection/initial_import_scripts/data/school_closure_order.csv")
        state_stay_in_place = pd.read_csv(settings.BASE_DIR + "/data_collection/initial_import_scripts/data/stay_in_place_order.csv")
        
        import_states(states)
        import_counties(counties)
        import_state_airports(state_airports)
        import_state_school_closures(state_school_closures)
        import_state_stay_in_place(state_stay_in_place)