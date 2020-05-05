from rest_framework import serializers
from covid_data.models import StateOutbreak, StateOutbreakCumulative, StateDailyFlights, StateStayInPlace, StateSchoolClosure


class StateOutbreakSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    
    class Meta:
        model = StateOutbreak
        fields = ['state', 'date', 'cases', 'negative_tests', 'total_tested', 'deaths', 'admitted_to_hospital', 'hospitalized', 'in_icu', 'days_since_outbreak']

class StateOutbreakCumulativeSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = StateOutbreakCumulative
        fields = ['state', 'date', 'cases', 'negative_tests', 'total_tested', 'deaths', 'hospitalized', 'in_icu', 'date_of_outbreak']

class StateStayInPlaceSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = StateStayInPlace
        fields = ['state', 'order', 'date']

class StateSchoolClosureSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = StateSchoolClosure
        fields = ['state', 'order', 'date']

class StateDailyFlightsSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = StateDailyFlights
        fields = ['state', 'date', 'number_of_inbound_flights', 'number_of_outbound_flights']

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['state_name', 'code', 'fips_code']