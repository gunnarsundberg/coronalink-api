import os
import requests
from random import random
import time as t
from itertools import repeat
from datetime import datetime, date, time , timedelta
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import pytz
from pytz import utc, timezone
from covid_data.models import Airport, DailyFlights, State
from covid_data.utilities import get_local_timestamp, api_request_from_str

username = os.environ['OPENSKY_USERNAME']
password = os.environ['OPENSKY_PASSWORD']   

def get_flights_by_region(region, flights_date):
    
    regional_airports = Airport.objects.filter(region=region)
    number_of_inbound_flights = 0
    number_of_outbound_flights = 0
    
    with ThreadPoolExecutor(max_workers=3) as e:
        futures = {e.submit(get_flights_by_airport, regional_airport, flights_date): regional_airport for regional_airport in regional_airports}
    
        for future in as_completed(futures):
            number_of_inbound_flights += (future.result()[0])
            number_of_outbound_flights += (future.result()[1])

    return number_of_inbound_flights, number_of_outbound_flights

def get_inbound_flights(inbound_flights_json):
    number_of_inbound_flights = 0
    try:
        for flight in inbound_flights_json:
            if flight:
                number_of_inbound_flights += 1
        return number_of_inbound_flights
    except:
        print("Couldn't get flight data")

def get_outbound_flights(outbound_flights_json):
    number_of_outbound_flights = 0
    try:
        for flight in outbound_flights_json:
            if flight:
                number_of_outbound_flights += 1
        return number_of_outbound_flights
    except:
        print("Couldn't get flight data")

def get_flights_by_airport(airport, flights_date):
    begin_timestamp, end_timestamp = get_local_timestamp(airport.timezone, flights_date)

    t.sleep(random())    
    inbound_flights_url = "https://" + username + ":" + password + "@opensky-network.org/api/flights/arrival?airport=" + str(airport.icao_code) + "&begin=" + str(begin_timestamp) + "&end=" + str(end_timestamp)
    t.sleep(random())
    outbound_flights_url = "https://" + username + ":" + password + "@opensky-network.org/api/flights/departure?airport=" + str(airport.icao_code) + "&begin=" + str(begin_timestamp) + "&end=" + str(end_timestamp)
    inbound_flights_json = api_request_from_str(inbound_flights_url)
    outbound_flights_json = api_request_from_str(outbound_flights_url)
        
    with ProcessPoolExecutor(max_workers=2) as p:
        inbound_flights_task = p.submit(get_inbound_flights, inbound_flights_json)
        outbound_flights_task = p.submit(get_outbound_flights, outbound_flights_json)
        
    number_of_inbound_flights = inbound_flights_task.result()
    number_of_outbound_flights = outbound_flights_task.result()

    return number_of_inbound_flights, number_of_outbound_flights

def update_regional_flights(region, date_to_update):
    try:
        number_of_inbound_flights, number_of_outbound_flights = get_flights_by_region(region, date_to_update)
        new_daily_flights = DailyFlights.objects.create(date=date_to_update, region=region, number_of_inbound_flights = number_of_inbound_flights, number_of_outbound_flights=number_of_outbound_flights)
        new_daily_flights.save()
    except:
        return

"""
def update_flights_daily():
    pass
"""