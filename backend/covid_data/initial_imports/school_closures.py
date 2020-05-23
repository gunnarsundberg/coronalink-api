import pandas as pd
from datetime import date
from covid_data.models import State, SchoolClosure

# Takes in pandas dataframe and adds state school closures
def import_state_school_closures(school_closure):
    for index, row in school_closure.iterrows():
        school_state_str = str(row['State'])
        school_closure_bool = (row['Instated'] == 1)
        school_date_of_order = row['Date of Order']
        school_state = State.objects.get(name=school_state_str)

        state_school_closure = SchoolClosure(order=school_closure_bool, date=school_date_of_order, region=school_state)
        state_school_closure.save()