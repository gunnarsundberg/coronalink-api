from __future__ import absolute_import, unicode_literals
from celery import task
from datetime import date
from covid_data.daily_updates.update_outbreak import update_all_state_outbreaks
from covid_data.initial_imports.outbreak_dependent_data import import_outbreak_dependent_data

def create_periodic_tasks():

@task()
def update_state_outbreak():
    date_to_update = date.today()
    update_all_state_outbreaks(date_to_update)

# State.objects.filter(update_timezone=)
@task()
def update_outbreak_dependent_data(region_set):
    import_outbreak_dependent_data(region_set)
