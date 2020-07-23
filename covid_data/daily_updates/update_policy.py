import pandas as pd
import io
import math
import requests
from datetime import date
from covid_data.models import DistancingPolicy, DistancingPolicyRollback, State, County

# List of available policy types
# See https://github.com/JieYingWu/COVID-19_US_County-level_Summaries
POLICY_TYPES = [
    ('stay at home', '0'),
    ('>50 gatherings', '1'),
    ('>500 gatherings', '2'),
    ('public schools', '3'),
    ('restaurant dine-in', '4'),
    ('entertainment/gym', '5')
]

# Updates both county and state distancing policies and rollbacks for all days available.
# See https://github.com/JieYingWu/COVID-19_US_County-level_Summaries
def update_policy():
    url = "https://raw.githubusercontent.com/gunnarsundberg/COVID-19_US_County-level_Summaries/master/data/interventions.csv"
    policy_data = requests.get(url).content
    policy_df = pd.read_csv(io.StringIO(policy_data.decode('utf-8')), dtype={'FIPS': 'object'})

    for index, row in policy_df.iterrows():
        fips = row['FIPS']
        # For each row in the policy csv, we must consider if the region is a county or a state, and for each, if they are a county/state that we track.
        # If the FIPS code ends in 3 zeros, it is not a county
        if fips[2:]=="000":
            # Try adding it as a state policy. If the FIPS code is not matched, flow will change to the except block
            try:
                fips = fips[:2]
                state = State.objects.get(fips_code=fips)
                # Check the row for all policy types
                for policy_type in POLICY_TYPES:
                    if not math.isnan(row[policy_type[0]]):
                        ordinal_date = (int(row[policy_type[0]]))
                        policy_date = date.fromordinal(ordinal_date)
                        new_policy, created = DistancingPolicy.objects.update_or_create(
                            region=state,
                            date=policy_date,
                            order_type=policy_type[1]
                        )
                        new_policy.save()
                    # Public schools have no rollback data currently
                    if policy_type[0] == 'public schools':
                        continue
                    # Check for rollbacks of the same policy type. It is assumed that there will only be a rollback if there is a policy first.
                    if not math.isnan(row[policy_type[0] + ' rollback']):
                        ordinal_date = (int(row[policy_type[0] + ' rollback']))
                        policy_date = date.fromordinal(ordinal_date)
                        new_rollback, created = DistancingPolicyRollback.objects.update_or_create(
                            policy=new_policy,
                            date=policy_date 
                        )
                        new_rollback.save()
            # Not a region we track. Continue to the next iteration
            except:
                continue
        # FIPS code follows county pattern
        else:
            try:
                if len(fips) == 5:
                    county = County.objects.get(fips_code=fips)
                    for policy_type in POLICY_TYPES:
                        if not math.isnan(row[policy_type[0]]):
                            ordinal_date = (int(row[policy_type[0]]))
                            policy_date = date.fromordinal(ordinal_date)
                            new_policy, created = DistancingPolicy.objects.update_or_create(
                                region=county,
                                order_type=policy_type[1],
                                defaults={'date': policy_date,}
                            )
                            new_policy.save()

                        if policy_type[0] == 'public schools':
                            continue

                        if not math.isnan(row[policy_type[0] + ' rollback']):
                            ordinal_date = (int(row[policy_type[0] + ' rollback']))
                            policy_date = date.fromordinal(ordinal_date)
                            new_rollback, created = DistancingPolicyRollback.objects.update_or_create(
                                policy=new_policy,
                                date=policy_date 
                            )
                            new_rollback.save()
            # Not a region we track. Continue to the next iteration
            except:
                continue