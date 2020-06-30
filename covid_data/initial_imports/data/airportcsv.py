import pandas as pd
import reverse_geocoder

labels = ['id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone_utc', 'dst', 'timezone_pytz', 'type', 'source']
airports = pd.read_csv("airports.csv", names=labels)

airports_primary = pd.read_csv("faa_primary_airports.csv")

states = pd.read_csv("states_final.csv")

# Get names of indexes for which column country does not have value United States
indexNames = airports[ airports['country'] != 'United States' ].index


# Delete these row indexes from dataFrame
airports.drop(indexNames , inplace=True)

# Remove airports with null ICAO
airports = airports[airports.icao.notnull()]

airports = airports.assign(in_primary=airports.icao.isin(airports_primary.ICAO).astype(int))

indexNames = airports[ airports['in_primary'] == 0 ].index
# Delete these row indexes from dataFrame
airports.drop(indexNames , inplace=True)

airports = airports.drop(columns=['in_primary'])

airports['state'] = ""

print(airports.head())

for index, row in airports.iterrows():
    latitude = row['latitude']
    longitude = row['longitude']
    coordinates = (latitude, longitude)

    #print(airports['latitude'].iloc[[0]])
    results = reverse_geocoder.search(coordinates)
    if results[0].get("admin1") == "Washington, D.C.":
        airports.at[index, 'state'] = "District of Columbia"
    else:
        airports.at[index, 'state'] = str(results[0].get("admin1"))


airports = airports.query('state in @states.State')


airports.drop(['id', 'city', 'latitude', 'longitude', 'altitude', 'dst', 'type', 'source', 'timezone_utc'], axis=1, inplace=True)


airports.to_csv('airports_usa.csv', index=False)