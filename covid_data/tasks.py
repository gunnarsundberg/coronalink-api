from __future__ import absolute_import, unicode_literals
from django.core.cache import cache
from celery import shared_task
import pytz
import requests
from concurrent.futures import ThreadPoolExecutor
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from datetime import datetime, date, time, timedelta
from covid_data.models import County, State, DailyWeather, DisplayDate, DailyFlights
from covid_data.daily_updates.update_outbreak import update_state_outbreak
from covid_data.daily_updates.update_weather import update_county_weather, update_state_weather
from covid_data.daily_updates.update_flights import update_regional_flights

cache_endpoints = [
    # Outbreak endpoint
    'outbreak/daily/states',
    'outbreak/cumulative/historic/states',

    # Flights endpoint
    'flights/daily/states',

    # Weather endpoint
    'weather/daily/states',
    'weather/daily/counties'
]

# Takes in state object and determines whether all counties in state have been updated. Returns boolean.
def all_counties_updated(state):
    current_display_date = DisplayDate.objects.all().latest('date').date
    for county in County.objects.filter(parent_region=state):
        if not current_display_date < DailyWeather.objects.filter(region=county).latest('date').date:
            return False
    return True

@shared_task
def update_state_outbreak_data():
    update_state_outbreak()

@shared_task
def clear_cache():
    cache.clear()

@shared_task
def create_daily_cache():
    for endpoint in cache_endpoints:
        requests.get('http://161.35.60.204/api/v1' + endpoint)

@shared_task
def update_display_date():
    previous_display_date = DisplayDate.objects.all().latest('date').date
    new_display_date = previous_display_date + timedelta(days=1)
    new_display_date_object = DisplayDate.objects.create(date=new_display_date)
    new_display_date_object.save()

@shared_task
def recover_county_data(start_date, end_date):
    iter_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    while iter_date <= end_date_datetime:
        with ThreadPoolExecutor() as e:
            for county in County.objects.all():
                e.submit(update_county_weather, county, iter_date)
        iter_date = iter_date + timedelta(days=1)

@shared_task
def recover_state_data(start_date, end_date):
    iter_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    while iter_date <= end_date_datetime:
        with ThreadPoolExecutor() as e:
            for state in State.objects.all():
                e.submit(update_state_weather, state, iter_date)
        iter_date = iter_date + timedelta(days=1)

    iter_date = datetime.strptime(start_date, "%Y-%m-%d")
    while iter_date <= end_date_datetime:
        for state in State.objects.all():
            update_regional_flights(state, iter_date)
        iter_date = iter_date + timedelta(days=1)

# TODO: In future, make updates dependent on date of latest outbreak record rather than assuming dates. Also, update days between if they were missed.
@shared_task
def update_county_data():
    previous_display_date = DisplayDate.objects.all().latest('date').date
    new_display_date = previous_display_date + timedelta(days=1)
    today = date.today()
    midnight = datetime.combine(today, time(hour=0, minute=30, second=0)) # We use 30 minutes past midnight on the day after the most current outbreak data (posted ~4pm EST) to be sure all other API's have full data for previous day
    
    # For each unique timezone in the US, check if it is past midnight and if outbreak dependent data needs to be updated.
    for county_tz in County.objects.all().values('timezone_str').distinct():
        tz_str = county_tz['timezone_str']
        tz = pytz.timezone(tz_str)
        midnight_local = midnight.replace(tzinfo=tz)
        now_local = tz.fromutc(datetime.utcnow())
        
        county_in_tz = County.objects.filter(timezone_str=tz_str)[0]
        # If midnight has passed and there are no existing weather records for the previous day, create them.
        if (now_local >= midnight_local and not DailyWeather.objects.filter(date=new_display_date).filter(region=county_in_tz).exists()):
            with ThreadPoolExecutor() as e:
                for county in County.objects.filter(timezone_str=tz_str):
                    e.submit(update_county_weather, county, new_display_date)

@shared_task
def update_state_data():
    previous_display_date = DisplayDate.objects.all().latest('date').date
    new_display_date = previous_display_date + timedelta(days=1)
    for state in State.objects.all():
        if all_counties_updated(state):
            if not DailyFlights.objects.filter(date=new_display_date).filter(region=state).exists() and not DailyWeather.objects.filter(date=new_display_date).filter(region=state).exists():
                update_regional_flights(state, new_display_date)
                update_state_weather(state, new_display_date)

def create_periodic_tasks():
    display_date_schedule = CrontabSchedule.objects.create(minute="10", hour="11")
    daily_cache_schedule = CrontabSchedule.objects.create(minute="11", hour="11")
    outbreak_schedule = CrontabSchedule.objects.create(minute="0", hour="2")
    outbreak_related_county_schedule = CrontabSchedule.objects.create(minute="30", hour="4, 5, 6, 7, 8, 9, 10")
    outbreak_related_state_schedule = CrontabSchedule.objects.create(minute="0", hour="5, 6, 7, 8, 9, 10, 11")
    
    PeriodicTask.objects.create(
        crontab=display_date_schedule,
        name='Update API display date',
        task='covid_data.tasks.update_display_date',
        enabled=True,
    )

    PeriodicTask.objects.create(
        crontab=outbreak_schedule,
        name='Nightly state outbreak update',
        task='covid_data.tasks.update_state_outbreak_data',
        enabled=True,
    )

    PeriodicTask.objects.create(
        crontab=outbreak_related_county_schedule,
        name='Nightly county outbreak-related data',
        task='covid_data.tasks.update_county_data',
        enabled=True,
    )

    PeriodicTask.objects.create(
        crontab=outbreak_related_state_schedule,
        name='Nightly state outbreak-related data',
        task='covid_data.tasks.update_state_data',
        enabled=True,
    )

    PeriodicTask.objects.create(
        crontab=display_date_schedule,
        name="Daily cache clear",
        task='covid_data.tasks.clear_cache',
        enabled=True,
    )

    PeriodicTask.objects.create(
        crontab=daily_cache_schedule,
        name="Create daily cache",
        task='covid_data.tasks.create_daily_cache',
        enabled=True
    )