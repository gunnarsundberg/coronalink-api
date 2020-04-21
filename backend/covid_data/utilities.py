from datetime import datetime, date, time , timedelta
import requests
import time as t
import pytz
from pytz import utc, timezone

# Helper function that takes in timezone and date and returns a unix timestamp for beginning of the day and end of the day
# Called by get_flights_by_state()
def get_local_timestamp(timezone_str, date):
    
    begin_datetime = datetime.combine(date, time(hour=0, minute=0, second=0))
    end_datetime = datetime.combine(date, time(hour=23, minute=59, second=59))

    region_timezone = timezone(timezone_str)
    
    begin_datetime = region_timezone.localize(begin_datetime)
    end_datetime = region_timezone.localize(end_datetime)

    utc_begin_datetime = begin_datetime.astimezone(utc)
    utc_end_datetime = end_datetime.astimezone(utc)

    return int(utc_begin_datetime.timestamp()), int(utc_end_datetime.timestamp())

# Takes in date string with no dashes and returns datetime object
def get_datetime_from_str(datetime_str):
    year = int(datetime_str[:4])
    month = int(datetime_str[4:6])
    day = int(datetime_str[6:8])
    return datetime(year=year, month=month, day=day)

# Takes in api url as str and returns json response
def api_request_from_str(url_str):
    for i in range(4):
        try:
            response = requests.get(url_str)
            return response.json()
        except:
            print("Unable to get data. Retrying..")
            t.sleep(5)