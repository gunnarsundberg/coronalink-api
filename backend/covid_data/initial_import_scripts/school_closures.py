import pandas as pd
from datetime import date
from covid_data.models import State, StateSchoolClosure

# Takes in pandas dataframe and adds state school closures
def import_state_school_closures(school_closure):
    for index, row in school_closure.iterrows():
        school_state_str = str(row['State'])
        school_closure_bool = (row['Instated'] == 1)
        school_date_of_order = row['Date of Order']
        school_state_object = State.objects.get(state_name=school_state_str)

        new_state_school_closure = StateSchoolClosure(order=school_closure_bool, date=school_date_of_order, state=school_state_object)
        new_state_school_closure.save()