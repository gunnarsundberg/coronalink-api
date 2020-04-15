import datetime
import requests
from data_collection.models import State, StateOutbreakCumulative, StateOutbreak
from data_collection.daily_update_scripts.update_outbreak import update_state_outbreak

states = States.objects.all()

for state in states:
    