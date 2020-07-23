import io
import requests
from datetime import datetime, date
import pandas as pd
from covid_data.models import State, County, MobilityTrends, DailyTrips

# Function to create individual DailyTrips records
def create_trips_record(region, date, row):
    population_at_home = row['Population Staying at Home']
    population_out_of_home = row['Population Not Staying at Home']
    total_trips = row['Number of Trips']
    trips_lt_1 = row['Number of Trips <1']
    trips_1_3 = row['Number of Trips 1-3']
    trips_3_5 = row['Number of Trips 3-5']
    trips_5_10 = row['Number of Trips 5-10']
    trips_10_25 = row['Number of Trips 10-25']
    trips_25_50 = row['Number of Trips 25-50']
    trips_50_100 = row['Number of Trips 50-100']
    trips_100_250 = row['Number of Trips 100-250']
    trips_250_500 = row['Number of Trips 250-500']
    trips_gt_500 = row['Number of Trips >=500']

    new_trips_record, created = DailyTrips.objects.update_or_create(
        region=region,
        date=date,
        defaults={
            'population_at_home'=population_at_home,
            'population_out_of_home'=population_out_of_home,
            'total_trips'=total_trips,
            'trips_lt_1'=trips_lt_1,
            'trips_1_3'=trips_1_3,
            'trips_3_5'=trips_3_5,
            'trips_5_10'=trips_5_10,
            'trips_10_25'=trips_10_25,
            'trips_25_50'=trips_25_50,
            'trips_50_100'=trips_50_100,
            'trips_100_250'=trips_100_250,
            'trips_250_500'=trips_250_500,
            'trips_gt_500'=trips_gt_500
        }
    )
    new_trips_record.save()

# Function to create individual MobilityTrends records.
def create_mobility_record(region, date, row):
    retail = row['retail_and_recreation_percent_change_from_baseline']
    grocery = row['grocery_and_pharmacy_percent_change_from_baseline']
    parks = row['parks_percent_change_from_baseline']
    transit = row['transit_stations_percent_change_from_baseline']
    workplace = row['workplaces_percent_change_from_baseline']
    residential = row['residential_percent_change_from_baseline']

    new_mobility, created = MobilityTrends.objects.update_or_create(
        date=date,
        region=region,
        defaults = {
            'retail_and_recreation_trend'=retail,
            'grocery_and_pharmacy_trend'=grocery,
            'parks_trend'=parks,
            'transit_trend'=transit,
            'workplace_trend'=workplace,
            'residential_trend'=residential
        }
    )
    new_mobility.save()

# Updates daily trips at the county and state level.
# For more info, see https://data.bts.gov/Research-and-Statistics/Trips-by-Distance/w96p-f2qv
def update_trips():
    url = "https://data.bts.gov/api/views/w96p-f2qv/rows.csv?accessType=DOWNLOAD"
    trips_data = requests.get(url).content
    trips_df = pd.read_csv(io.StringIO(trips_data.decode('utf-8')), dtype={'County FIPS': 'object'})
    trips_df = trips_df.query("Level == 'County' or Level == 'State'")
    for index, row in trips_df.iterrows():
        date = datetime.strptime(row['Date'], "%Y/%m/%d").date()
        try:
            if row['Level'] == 'County':
                county = County.objects.get(fips_code=row['County FIPS'])
                create_trips_record(region=county, date=date, row=row)
            if row['Level'] == 'State':
                state = State.objects.get(code=row['State Postal Code'])
                create_trips_record(region=state, date=date, row=row)
        except:
            continue
        
# Updates mobility trends for all states and counties in the US
# For more information on mobility data, see https://www.google.com/covid19/mobility/data_documentation.html?hl=en
def update_mobility_trends():
    url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
    mobility_data = requests.get(url).content
    mobility_df = pd.read_csv(io.StringIO(mobility_data.decode('utf-8')), dtype={'census_fips_code': 'object', 'sub_region_2': 'object'})
    mobility_df = mobility_df.query("country_region_code == 'US'")

    for index, row in mobility_df.iterrows():
        date = datetime.strptime(row['date'], "%Y-%m-%d").date()
        try:
            # sub_region_2 is for counties. If null, this is a state-level record.
            if pd.isnull(row['sub_region_2']):
                state = State.objects.get(name=row['sub_region_1'])
                create_mobility_record(region=state, date=date, row=row)
            else:
                county = County.objects.get(fips_code=row['census_fips_code'])
                create_mobility_record(region=county, date=date, row=row)
        except:
            continue