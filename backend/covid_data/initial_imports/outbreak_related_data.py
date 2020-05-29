from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from covid_data.models import State, County, Outbreak, DisplayDate
from covid_data.daily_updates.update_flights import update_regional_flights
from covid_data.daily_updates.update_weather import update_county_weather, update_state_weather

def import_outbreak_related_data(states):
    states_bar = tqdm(desc="Importing Outbreak-related Data", total=states.count())
    for i, state in enumerate(states):
        state_outbreak = Outbreak.objects.filter(region=state)
        
        data_bar = tqdm(desc="Outbreak-related data for {}".format(state.name), total=state_outbreak.count(), leave=False)
        for outbreak_record in state_outbreak:
            date_to_update = outbreak_record.date

            if date_to_update <= DisplayDate.objects.all().latest('date').date:
                state_counties = County.objects.filter(parent_region=state)

                with ThreadPoolExecutor() as e:
                    e.submit(update_regional_flights, state, date_to_update)
                    for county in state_counties:
                        e.submit(update_county_weather, county, date_to_update)

                update_state_weather(state, date_to_update)
                            
            data_bar.update(1)
        data_bar.close()
        states_bar.update(1)