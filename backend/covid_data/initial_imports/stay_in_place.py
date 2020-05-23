import pandas as pd
from datetime import date
from covid_data.models import State, StayInPlace

def import_state_stay_in_place(stay_in_place):
    for index, row in stay_in_place.iterrows():
        state_name = str(row['State'])
        order_bool = (row['Instated'] == 1)
        date_of_order = row['Date of Order']
        state = State.objects.get(name=state_name)

        state_stay_in_place = StayInPlace(order=order_bool, date=date_of_order, region=state)
        state_stay_in_place.save()