import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from covid_data.models import State, County, Demographics, CountyUrbanRelation, Outbreak, OutbreakCumulative, DistancingPolicy, DistancingPolicyRollback, MobilityTrends, DailyTrips, DailyFlights, DailyWeather
from covid_data.daily_updates.update_policy import POLICY_TYPES

def get_policy(index, row):
    county = County.objects.get(id=row['region'])
    date = row['date']
    result = {'index': str(index)}
    for policy_type in POLICY_TYPES:
        policy_value = None
        try:
            policy = DistancingPolicy.objects.filter(region=county).get(order_type=policy_type[1])
            try:
                if date >= policy.date and date < DistancingPolicyRollback.objects.get(policy=policy).date:
                    policy_value = True
                else:
                    policy_value = False
            except:
                if date >= policy.date:
                    policy_value = True
                else:
                    policy_value = False 
        except:
            policy_value = False
            
        result.update({str(policy_type[0]): policy_value})

def update_policy_value(county_df, record):
    for policy_type in POLICY_TYPES:
        county_df.loc[policy_type[0], record['index']] = record[policy_type[0]]

def export_county_data():
    # Get dataframes for features
    outbreak_cumulative_df = OutbreakCumulative.as_dataframe(queryset=OutbreakCumulative.objects.filter(region__in=County.objects.all()))
    demographics_df = Demographics.as_dataframe(queryset=Demographics.objects.filter(region__in=County.objects.all()))
    urban_df = CountyUrbanRelation.as_dataframe()
    mobility_df = MobilityTrends.as_dataframe(queryset=MobilityTrends.objects.filter(region__in=County.objects.all()))
    trips_df = DailyTrips.as_dataframe(queryset=DailyTrips.objects.filter(region__in=County.objects.all()))
    weather_df = DailyWeather.as_dataframe(queryset=DailyWeather.objects.filter(region__in=County.objects.all()))

    # Merge dataframes
    outbreak_mobility_merge = pd.merge(outbreak_cumulative_df, pd.merge(mobility_df, trips_df, how='left', on=['region', 'date']), how='left', on=['region', 'date'])
    daily_data = pd.merge(outbreak_mobility_merge, weather_df, how='left', on=['region', 'date'])
    demographics_merge = pd.merge(demographics_df, urban_df, how='left', left_on='region', right_on='county')
    county_df = pd.merge(daily_data, demographics_merge, how='left', on='region')
    
    # Drop id columns
    cols = [c for c in county_df.columns if c[:2] != 'id']
    county_df = county_df[cols]
    print(county_df)
    
    # Drop columns not relevant to county data
    county_df = county_df.drop(labels=['county', 'negative_tests', 'total_tested', 'hospitalized', 'in_icu'], axis=1)
    county_df = county_df.sort_values(by=['region', 'date'])
    
    # Add policy columns
    for policy_type in POLICY_TYPES:
        county_df.insert(column=policy_type[0], value=None, loc=12)

    policy_results = []

    with ThreadPoolExecutor() as e:
        for index, row in county_df.iterrows():
            future = e.submit(get_policy, index, row)
            policy_results.append(future.result())
        #e.shutdown(wait=True)

    print(policy_results)

    with ThreadPoolExecutor() as p:
        for record in policy_results:
            p.submit(update_policy_value, county_df, record)
        p.shutdown(wait=True)

    os.chdir(settings.BASE_DIR)
    county_df.to_csv("data/county_data.csv")
    #os.system('git add data/county_data.csv && git push')
    # TODO: add policies for all rows
    #policy_df = DistancingPolicy.as_dataframe()
    return county_df

def export_state_data():
    flights_df = DailyFlights.as_dataframe()