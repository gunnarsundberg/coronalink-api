from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from covid_data.models import State, County, Outbreak
from covid_data.daily_updates.update_flights import update_regional_flights
from covid_data.daily_updates.update_weather import update_county_weather

def import_outbreak_dependent_data(states):
    states_bar = tqdm(desc="Importing Outbreak-related Data", total=states.count())
    for i, state in enumerate(states):
        state_outbreak = Outbreak.objects.filter(region=state)
        
        data_bar = tqdm(desc="Outbreak-related data for {}".format(state.name), total=state_outbreak.count(), leave=False)
        for outbreak_record in state_outbreak:
                date_to_update = outbreak_record.date

                #update_state_flights(state, date_to_update)
                
                state_counties = County.objects.filter(parent_region=state)

                with ThreadPoolExecutor() as e:
                    
                    weather_bar = tqdm(desc="County Weather for {} on {}".format(state.name, str(date_to_update)), total=state_counties.count(), leave=False)
                    for county in state_counties:
                        e.submit(update_county_weather, county, date_to_update)
                        weather_bar.update(1)
                    weather_bar.close()
                data_bar.update(1)
        
        states_bar.update(1)