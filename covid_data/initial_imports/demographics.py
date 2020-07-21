from django.conf import settings
from concurrent.futures import ThreadPoolExecutor
from covid_data.models import State, County, Demographics, CountyUrbanRelation
from covid_data.utilities import api_request_from_str
from tqdm import tqdm
import pandas as pd
import os
import threading

COUNTY_BASE_URL = "https://api.census.gov/data/2018/acs/acs5?key=" + os.environ['CENSUS_API_KEY'] + "&get={0}&for=county:{1}&in=state:{2}"
STATE_BASE_URL = "https://api.census.gov/data/2018/acs/acs5?key=" + os.environ['CENSUS_API_KEY'] + "&get={0}&for=state:{1}"

DEMOGRAPHIC_CODES = {
    "population": "B01001_001E",  # TotalPopulation
    "male": "B01001_002E",  # NumMale
    "female": "B01001_026E",  # Numfemale
    "median_age": "B01002_001E",  # MedianAge

    "male_60_61": "B01001_018E",  # Num Male Age 60-61
    "male_62_64": "B01001_019E",  # 62-64
    "male_65_66": "B01001_020E",  # 65-66
    "male_67_69": "B01001_021E",  # 67-69
    "male_70_74": "B01001_022E",  # 70-74
    "male_75_79": "B01001_023E",  # 75-79
    "male_80_84": "B01001_024E",  # 80-84
    "male_85_plus": "B01001_025E",  # 85+

    "female_60_61": "B01001_042E",  # Num female Age 60-61
    "female_62_64": "B01001_043E",  # 62-64
    "female_65_66": "B01001_044E",  # 65-66
    "female_67_69": "B01001_045E",  # 67-69
    "female_70_74": "B01001_046E",  # 70-74
    "female_75_79": "B01001_047E",  # 75-79
    "female_80_84": "B01001_048E",  # 80-84
    "female_85_plus": "B01001_049E",  # 85+
}

def get_county_demographics(county):
    with ThreadPoolExecutor() as e:
        # Population by male and female
        male_population_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male'], str(county.fips_code[2:5]), str(county.fips_code)[0:2]))
        female_population_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))

        # Get male data for 60s-80+ in increments provided by census
        male_60_61_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male_60_61'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        male_62_64_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male_62_64'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        male_65_66_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male_65_66'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        male_67_69_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male_67_69'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        male_70_74_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male_70_74'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        male_75_79_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male_75_79'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        male_80_85_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male_80_84'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        male_85_plus_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['male_85_plus'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        
        # Get female data for 60s-80 plus in increments provided by census
        female_60_61_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female_60_61'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        female_62_64_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female_62_64'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        female_65_66_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female_65_66'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        female_67_69_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female_67_69'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        female_70_74_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female_70_74'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        female_75_79_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female_75_79'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        female_80_85_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female_80_84'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        female_85_plus_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['female_85_plus'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))

        # Get data as it will be stored
        population_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['population'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))
        median_age_task = e.submit(api_request_from_str, COUNTY_BASE_URL.format(DEMOGRAPHIC_CODES['median_age'], str(county.fips_code)[2:5], str(county.fips_code)[0:2]))

    male_population = male_population_task.result()
    female_population = female_population_task.result()

    male_60_61= male_60_61_task.result()
    male_62_64 = male_62_64_task.result()
    male_65_66 = male_65_66_task.result()
    male_67_69 = male_67_69_task.result()
    male_70_74 = male_70_74_task.result()
    male_75_79 = male_75_79_task.result()
    male_80_85 = male_80_85_task.result()
    male_85_plus = male_85_plus_task.result()
        
    female_60_61 = female_60_61_task.result()
    female_62_64 = female_62_64_task.result()
    female_65_66 = female_65_66_task.result()
    female_67_69 = female_67_69_task.result()
    female_70_74 = female_70_74_task.result()
    female_75_79 = female_75_79_task.result()
    female_80_85 = female_80_85_task.result()
    female_85_plus = female_85_plus_task.result()

    population = population_task.result()
    median_age = median_age_task.result()
    
    population_density = round(int((population[1][0]))/county.land_area, 1)
    population = int((population[1][0]))
    median_age = float((median_age[1][0]))
    percent_male = round((int((male_population[1][0])))/population, 3) * 100
    percent_female = round((int((female_population[1][0])))/population, 3) * 100
    percent_60s = round((int((male_60_61[1][0])) + int((male_62_64[1][0])) + int((male_67_69[1][0])) + int((female_60_61[1][0])) + int((female_62_64[1][0])) + int((female_65_66[1][0])) + int((female_67_69[1][0])))/population, 3) * 100
    percent_70s = round((int((male_70_74[1][0])) + int((male_75_79[1][0])) + int((female_70_74[1][0])) + int((female_75_79[1][0])))/population, 3) * 100
    percent_80_plus = round((int((male_80_85[1][0])) + int((male_85_plus[1][0])) + int((female_80_85[1][0])) + int((female_85_plus[1][0])))/population, 3) * 100

    county_demographics = Demographics.objects.create(
        region=county, 
        population=population, 
        median_age=median_age, 
        percent_male=percent_male, 
        percent_female=percent_female, 
        percent_60s=percent_60s, 
        percent_70s=percent_70s, 
        percent_80_plus=percent_80_plus, 
        population_density=population_density
    )
    county_demographics.save()

def get_state_demographics(state):
    # Population by male and female
    male_population = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male'], str(state.fips_code)))[1][0])
    female_population = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female'], str(state.fips_code)))[1][0])

    # Get male data for 60s-80 plus in increments provided by census
    male_60_61 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male_60_61'], str(state.fips_code)))[1][0])
    male_62_64 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male_62_64'], str(state.fips_code)))[1][0])
    male_65_66 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male_65_66'], str(state.fips_code)))[1][0])
    male_67_69 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male_67_69'], str(state.fips_code)))[1][0])
    male_70_74 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male_70_74'], str(state.fips_code)))[1][0])
    male_75_79 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male_75_79'], str(state.fips_code)))[1][0])
    male_80_85 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male_80_84'], str(state.fips_code)))[1][0])
    male_85_plus = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['male_85_plus'], str(state.fips_code)))[1][0])
    
    # Get female data for 60s-80 plus in increments provided by census
    female_60_61 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female_60_61'], str(state.fips_code)))[1][0])
    female_62_64 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female_62_64'], str(state.fips_code)))[1][0])
    female_65_66 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female_65_66'], str(state.fips_code)))[1][0])
    female_67_69 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female_67_69'], str(state.fips_code)))[1][0])
    female_70_74 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female_70_74'], str(state.fips_code)))[1][0])
    female_75_79 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female_75_79'], str(state.fips_code)))[1][0])
    female_80_85 = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female_80_84'], str(state.fips_code)))[1][0])
    female_85_plus = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['female_85_plus'], str(state.fips_code)))[1][0])

    # Get data as it will be stored
    population = int(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['population'], str(state.fips_code)))[1][0])
    median_age = float(api_request_from_str(STATE_BASE_URL.format(DEMOGRAPHIC_CODES['median_age'], str(state.fips_code)))[1][0])
    population_density = round(population/state.land_area, 1)
    percent_male = round(male_population/population, 3) * 100
    percent_female = round(female_population/population, 3) * 100
    percent_60s = round((male_60_61 + male_62_64 + male_67_69 + female_60_61 + female_62_64 + female_65_66 + female_67_69)/population, 3) * 100
    percent_70s = round((male_70_74 + male_75_79 + female_70_74 + female_75_79)/population, 3) * 100
    percent_80_plus = round((male_80_85 + male_85_plus + female_80_85 + female_85_plus)/population, 3) * 100

    state_demographics = Demographics.objects.create(
        region=state, 
        population=population, 
        median_age=median_age, 
        percent_male=percent_male, 
        percent_female=percent_female, 
        percent_60s=percent_60s, 
        percent_70s=percent_70s, 
        percent_80_plus=percent_80_plus, 
        population_density=population_density
    )
    state_demographics.save()

def import_county_demographics():
    progress_bar = tqdm(desc="Importing County Demographics", total=County.objects.count())
    for county in County.objects.all():
        get_county_demographics(county)
        progress_bar.update(1)

def import_state_demographics():
    progress_bar = tqdm(desc="Importing State Demographics", total=State.objects.count())
    for state in State.objects.all():
        get_state_demographics(state)
        progress_bar.update(1)

# Imports Rural-Urban Continuum and Urban Influence codes for all counties in the US
# For Rural-Urban Continuum information, see https://www.ers.usda.gov/data-products/rural-urban-continuum-codes//
# For Urban Influence information, see https://www.ers.usda.gov/data-products/urban-influence-codes.aspx
def import_county_urban_relations():
    outbreak_data = pd.read_csv(settings.BASE_DIR + "/covid_data/initial_imports/data/poverty_urban_codes.csv", dtype={'FIPStxt': 'object', 'Rural-urban_Continuum_Code_2013': 'object', 'Urban_Influence_Code_2013': 'object'})

    for index, row in outbreak_data.iterrows():
        fips = row['FIPStxt']
        if fips[2:]=="000":
            try:
                fips = fips[:2]
                state = State.objects.get(fips_code=fips)
                state_demographics = Demographics.objects.get(region=state)
                state_demographics.total_poverty = row['POVALL_2018']
                state_demographics.percent_poverty = row['PCTPOVALL_2018']
                state_demographics.save()
            except:
                continue
        else:
            county = County.objects.get(fips_code=fips)
            urban_relation = CountyUrbanRelation.objects.create(
                county=county,
                urban_continuum_code=row['Rural-urban_Continuum_Code_2013'],
                urban_influence_code=row['Urban_Influence_Code_2013']
            )
            urban_relation.save()

            county_demographics = Demographics.objects.get(region=county)
            county_demographics.total_poverty = row['POVALL_2018']
            county_demographics.percent_poverty = row['PCTPOVALL_2018']
            county_demographics.save()    