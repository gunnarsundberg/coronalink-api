import pandas as pd

states = pd.read_csv("states.csv")

states.drop(['Abbrev'], axis=1, inplace=True)

states.to_csv('states_final.csv', index=False)