from datetime import datetime, date, time , timedelta
import requests
import time as t
import pytz
from pytz import utc, timezone
from timezonefinder import TimezoneFinder

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

def get_local_timezone(lat, lon):
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lon, lat=lat)

# Takes in date string with no dashes and returns datetime object
def get_datetime_from_str(datetime_str):
    year = int(datetime_str[:4])
    month = int(datetime_str[4:6])
    day = int(datetime_str[6:8])
    return date(year=year, month=month, day=day)

class FailedRequest(Exception):
    """Exception raised for errors in JSON requests.

    Attributes:
        response -- response object which caused the error
        message -- explanation of the error
    """

    def __init__(self, response, message="Request failed or did not return a JSON response."):
        self.response = response
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} Response code: {self.response.status_code} Response content: {self.response.text}'

# Takes in api url as str and returns json response
def api_request_from_str(url_str):
    # Try request 4 times, waiting 2 seconds between each failed attempt.
    for i in range(5):
        try:
            response = requests.get(url_str)
            if response.status_code == 200:
                return response.json()
            else:
                raise FailedRequest(response)
        except:
            t.sleep(2)

    response = requests.get(url_str)
    if response.status_code == 200:
        return response.json()
    else:
        raise FailedRequest(response)