import os
import pandas as pd
from datetime import datetime, date
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from django.conf import settings
from covid_data.models import State, County, Demographics, CountyUrbanRelation, Outbreak, OutbreakCumulative, DistancingPolicy, DistancingPolicyRollback, MobilityTrends, DailyTrips, DailyFlights, DailyWeather
from covid_data.daily_updates.update_policy import POLICY_TYPES

def update_region_policies(region, region_df, region_policies, rollback_qs):
    for policy_type in POLICY_TYPES:
            try:
                policy = region_policies.get(order_type=policy_type[1])
                try:
                    rollback = rollback_qs.get(policy=policy)
                    region_df.loc[((region_df.region == region.id) & (region_df.date >= policy.date) & (region_df.date < rollback.date)), policy_type[0]] = True
                    region_df.loc[((region_df.region == region.id) & ((region_df.date < policy.date) | (region_df.date >= rollback.date))), policy_type[0]] = False
                except:
                    region_df.loc[(region_df.region == region.id & region_df.date >= policy.date), policy_type[0]] = True
                    region_df.loc[(region_df.region == region.id & region_df.date < policy.date), policy_type[0]] = False
            except:
                region_df.loc[(region_df.region == region.id), policy_type[0]] = False

def export_county_data():
    # Get dataframes for features
    county_qs = County.objects.all()
    policy_qs = DistancingPolicy.objects.all()
    rollback_qs = DistancingPolicyRollback.objects.all()

    outbreak_cumulative_df = OutbreakCumulative.as_dataframe(queryset=OutbreakCumulative.objects.filter(region__in=county_qs))
    outbreak_df = Outbreak.as_dataframe(queryset=Outbreak.objects.filter(region__in=county_qs))
    demographics_df = Demographics.as_dataframe(queryset=Demographics.objects.filter(region__in=county_qs))
    urban_df = CountyUrbanRelation.as_dataframe()
    mobility_df = MobilityTrends.as_dataframe(queryset=MobilityTrends.objects.filter(region__in=county_qs))
    trips_df = DailyTrips.as_dataframe(queryset=DailyTrips.objects.filter(region__in=county_qs))
    weather_df = DailyWeather.as_dataframe(queryset=DailyWeather.objects.filter(region__in=county_qs))
    county_df = County.as_dataframe(field_list=['id', 'name', 'parent_region', 'fips_code'])
    state_df = State.as_dataframe(field_list=['id', 'code'])

    # Merge dataframes
    regional_merge = pd.merge(county_df, state_df, how='left', left_on='parent_region', right_on='id')

    outbreak_merge = pd.merge(outbreak_cumulative_df[['region', 'date', 'date_of_outbreak', 'days_since_outbreak', 'cases', 'deaths']], outbreak_df[['cases', 'deaths', 'case_adjacency_risk', 'region', 'date']], on=['region', 'date'], suffixes=("_cumulative", "_new"))
    outbreak_mobility_merge = pd.merge(outbreak_merge, pd.merge(mobility_df, trips_df, how='left', on=['region', 'date']), how='left', on=['region', 'date'])
    daily_data = pd.merge(outbreak_mobility_merge, weather_df, how='left', on=['region', 'date'])
    demographics_merge = pd.merge(demographics_df, urban_df, how='left', left_on='region', right_on='county')
    county_merge = pd.merge(demographics_merge, regional_merge[['id_x', 'name', 'code', 'fips_code']], how='left', left_on='region', right_on='id_x')
    county_data_df = pd.merge(daily_data, county_merge, how='left', on='region')

    

    # Drop id columns
    cols = [c for c in county_data_df.columns if c[:2] != 'id']
    county_data_df = county_data_df[cols]
    print(county_data_df)
    
    # Drop columns not relevant to county data
    county_df = county_df.drop(labels=['county'], axis=1)
    county_data_df = county_data_df.drop_duplicates()
    county_data_df = county_data_df.sort_values(by=['region', 'date'])
    
    # Add policy columns
    for policy_type in POLICY_TYPES:
        county_data_df.insert(column=policy_type[0], value=None, loc=15)

    #with ProcessPoolExecutor() as p:
    for county in county_qs:
        county_policies = policy_qs.filter(region=county)
        update_region_policies(county, county_data_df, county_policies, rollback_qs)

    # Rename columns
    county_data_df.rename(columns = {'name':'county', 'code':'state'}, inplace = True)

    # Change order
    county_data_df = county_data_df[[
        'county',
        'state', 
        'fips_code',
        'date', 
        'date_of_outbreak', 
        'days_since_outbreak',
       'cases_cumulative', 
       'deaths_cumulative', 
       'cases_new', 
       'deaths_new',
       'case_adjacency_risk', 
       'retail_and_recreation_trend',
       'grocery_and_pharmacy_trend', 
       'parks_trend', 
       'transit_trend',
       'workplace_trend', 
       'residential_trend', 
       'entertainment/gym',
       'restaurant dine-in', 
       'public schools', 
       '>500 gatherings',
       '>50 gatherings', 
       'stay at home', 
       'population_at_home',
       'population_out_of_home', 
       'total_trips', 
       'trips_lt_1', 
       'trips_1_3',
       'trips_3_5', 
       'trips_5_10', 
       'trips_10_25', 
       'trips_25_50', 
       'trips_50_100',
       'trips_100_250', 
       'trips_250_500', 
       'trips_gt_500', 
       'avg_temperature',
       'max_temperature', 
       'min_temperature', 
       'avg_humidity', 
       'uv_index',
       'population', 
       'population_density', 
       'percent_male', 
       'percent_female',
       'median_age', 
       'percent_60s', 
       'percent_70s', 
       'percent_80_plus',
       'total_poverty', 
       'percent_poverty', 
       'urban_continuum_code',
       'urban_influence_code',
       'region'
       ]]
       
    # Export
    county_data_df.to_csv(settings.BASE_DIR + "/data/county_data.csv", index=False)
    return county_data_df

def export_state_data():
    flights_df = DailyFlights.as_dataframe()