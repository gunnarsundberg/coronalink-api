import os
import requests
import time as t
from datetime import datetime, date, time , timedelta
import pytz
from pytz import utc, timezone
from data_collection.models import StateAirport, StateDailyFlights, State

username = os.environ['OPENSKY_USERNAME']
password = os.environ['OPENSKY_PASSWORD']

# Helper function that takes in timezone and date and returns a unix timestamp for beginning of the day and end of the day
# Called by get_flights_by_state()
def get_local_timestamp(airport_timezone_str, flight_date):
    
    begin_datetime = datetime.combine(flight_date, time(hour=0, minute=0, second=0))
    end_datetime = datetime.combine(flight_date, time(hour=23, minute=59, second=59))

    airport_timezone = timezone(airport_timezone_str)
    
    begin_datetime = airport_timezone.localize(begin_datetime)
    end_datetime = airport_timezone.localize(end_datetime)

    utc_begin_datetime = begin_datetime.astimezone(utc)
    utc_end_datetime = end_datetime.astimezone(utc)

    return int(utc_begin_datetime.timestamp()), int(utc_end_datetime.timestamp())
    

def get_flights_by_state(state, flights_date):
    number_of_inbound_flights = 0
    number_of_outbound_flights = 0

    state_airports = StateAirport.objects.filter(state=state)

    for airport in state_airports:
        begin_timestamp, end_timestamp = get_local_timestamp(airport.timezone, flights_date)
        
        inbound_flights_request_str = "https://" + username + ":" + password + "@opensky-network.org/api/flights/arrival?airport=" + str(airport.icao_code) + "&begin=" + str(begin_timestamp) + "&end=" + str(end_timestamp)
        outbound_flights_request_str = "https://" + username + ":" + password + "@opensky-network.org/api/flights/departure?airport=" + str(airport.icao_code) + "&begin=" + str(begin_timestamp) + "&end=" + str(end_timestamp)
        
        inbound_flights = requests.get(inbound_flights_request_str)
        outbound_flights = requests.get(outbound_flights_request_str)

        try:
            inbound_flights_json = inbound_flights.json()
            outbound_flights_json = outbound_flights.json()
        except:
            print("Request failed. Retrying...")
            t.sleep(5)
            inbound_flights = requests.get(inbound_flights_request_str)
            outbound_flights = requests.get(outbound_flights_request_str)
            inbound_flights_json = inbound_flights.json()
            outbound_flights_json = outbound_flights.json()
        
        print()
        print("State: " + str(state.state_name))
        print("Airport: " + str(airport.airport_name))
        print(inbound_flights_request_str)
        print(inbound_flights_json)
        print(outbound_flights_json)
        print("Inbound flights before: " + str(number_of_inbound_flights))
        
        for flight in inbound_flights_json:
            if flight:
                number_of_inbound_flights += 1
        for flight in outbound_flights_json:
            if flight:
                number_of_outbound_flights += 1
        
        print("Inbound flights after: " + str(number_of_inbound_flights))
        print()

    return number_of_inbound_flights, number_of_outbound_flights

def import_flights(flights_date):
    
    states = State.objects.all()
    print(flights_date)
    
    for state in states:
        number_of_inbound_flights, number_of_outbound_flights = get_flights_by_state(state, flights_date)
        new_daily_flights = StateDailyFlights.objects.create(date=flights_date, state=state, number_of_inbound_flights = number_of_inbound_flights, number_of_outbound_flights=number_of_outbound_flights)
        print(new_daily_flights.date)
        new_daily_flights.save()

def update_flights_daily():
    yesterday = date.today() - timedelta(days = 1)
    print(yesterday)
    import_flights(yesterday)