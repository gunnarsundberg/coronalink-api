import pandas as pd
import reverse_geocoder

labels = ['id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone_utc', 'dst', 'timezone_pytz', 'type', 'source']
airports = pd.read_csv("airports.csv", names=labels)

states = pd.read_csv("states.csv")

# Get names of indexes for which column country has value United States
indexNames = airports[ airports['country'] != 'United States' ].index


# Delete these row indexes from dataFrame
airports.drop(indexNames , inplace=True)

airports = airports[airports.iata.notnull()]

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