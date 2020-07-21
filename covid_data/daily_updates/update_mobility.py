import io
import requests
from datetime import datetime, date
import pandas as pd
from covid_data.models import State, County, MobilityTrends

def update_trips():
    url = "https://data.bts.gov/api/views/w96p-f2qv/rows.csv?accessType=DOWNLOAD"
    trips_data = requests.get(url).content
    trips_df = pd.read_csv(io.StringIO(trips_data.decode('utf-8')), dtype={'County FIPS': 'object'})
    # For numbers with commas
    s = s.replace(',', '')

def update_mobility_trends():
    url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
    mobility_data = requests.get(url).content
    mobility_df = pd.read_csv(io.StringIO(mobility_data.decode('utf-8')), dtype={'census_fips_code': 'object', 'sub_region_2': 'object'})
    mobility_df = mobility_df.query("country_region_code == 'US'")

    for index, row in mobility_df.iterrows():
        date = datetime.strptime(row['date'], "%Y-%m-%d").date()
        # Sub Region 2 is for counties. If null, this is a state-level record
        if pd.isnull(row['sub_region_2']):
            try:
                state = State.objects.get(name=row['sub_region_1'])

                retail = row['retail_and_recreation_percent_change_from_baseline']
                grocery = row['grocery_and_pharmacy_percent_change_from_baseline']
                parks = row['parks_percent_change_from_baseline']
                transit = row['transit_stations_percent_change_from_baseline']
                workplace = row['workplaces_percent_change_from_baseline']
                residential = row['residential_percent_change_from_baseline']

                new_mobility, created = MobilityTrends.objects.update_or_create(
                    date=date,
                    region=state,
                    retail_and_recreation_trend=retail,
                    grocery_and_pharmacy_trend=grocery,
                    parks_trend=parks,
                    transit_trend=transit,
                    workplace_trend=workplace,
                    residential_trend=residential
                )
                new_mobility.save()

            except:
                print(row['sub_region_1'])
            
        else:
            try:
                county = County.objects.get(fips_code=row['census_fips_code'])
                
                retail = row['retail_and_recreation_percent_change_from_baseline']
                grocery = row['grocery_and_pharmacy_percent_change_from_baseline']
                parks = row['parks_percent_change_from_baseline']
                transit = row['transit_stations_percent_change_from_baseline']
                workplace = row['workplaces_percent_change_from_baseline']
                residential_trend = row['residential_percent_change_from_baseline']

                new_mobility, created = MobilityTrends.objects.update_or_create(
                    date=date,
                    region=county,
                    retail_and_recreation_trend=retail,
                    grocery_and_pharmacy_trend=grocery,
                    parks_trend=parks,
                    transit_trend=transit,
                    workplace_trend=workplace,
                    residential_trend=residential
                )
                new_mobility.save()

            except:
                print(row['sub_region_2'])