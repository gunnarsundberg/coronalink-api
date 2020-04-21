from rest_framework import serializers
from covid_data.models import StateOutbreak, StateOutbreakCumulative, StateDailyFlights, StateStayInPlace, StateSchoolClosure


class StateOutbreakSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.StringRelatedField()
    
    class Meta:
        model = StateOutbreak
        fields = ['state', 'date', 'cases', 'negative_tests', 'total_tested', 'deaths', 'admitted_to_hospital', 'hospitalized', 'in_icu', 'days_since_outbreak']

class StateOutbreakCumulativeSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = StateOutbreakCumulative
        fields = ['state', 'date', 'cases', 'negative_tests', 'total_tested', 'deaths', 'hospitalized', 'in_icu', 'date_of_outbreak']

class StateStayInPlaceSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = StateStayInPlace
        fields = ['state', 'order', 'date']

class StateSchoolClosureSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.StringRelatedField()

    class Meta:
        model = StateSchoolClosure
        fields = ['state', 'order', 'date']

class StateDailyFlightsSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.StringRelatedField()
    
    class Meta:
        model = StateDailyFlights
        fields = ['state', 'number_of_inbound_flights', 'number_of_outbound_flights']