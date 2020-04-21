import pandas as pd
from datetime import date
from covid_data.models import State, StateStayInPlace

def import_state_stay_in_place(stay_in_place):
    for index, row in stay_in_place.iterrows():
        stay_in_place_state_str = str(row['State'])
        stay_in_place_bool = (row['Instated'] == 1)
        stay_in_place_date_of_order = row['Date of Order']
        stay_in_place_state_object = State.objects.get(state_name=stay_in_place_state_str)

        new_state_stay_in_place = StateStayInPlace(order=stay_in_place_bool, date=stay_in_place_date_of_order, state=stay_in_place_state_object)
        new_state_stay_in_place.save()