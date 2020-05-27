from rest_framework import serializers
from covid_data.models import State, Outbreak, OutbreakCumulative, DailyFlights, StayInPlace, SchoolClosure, Demographics, DailyWeather

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['name', 'code', 'fips_code']

class StateOutbreakSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state') #StateSerializer(source='region.state')

    class Meta:
        model = Outbreak
        fields = ['state', 'date', 'cases', 'negative_tests', 'total_tested', 'deaths', 'admitted_to_hospital', 'hospitalized', 'in_icu', 'days_since_outbreak']

class StateOutbreakCumulativeSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state')

    class Meta:
        model = OutbreakCumulative
        fields = ['state', 'date', 'cases', 'negative_tests', 'total_tested', 'deaths', 'hospitalized', 'in_icu', 'days_since_outbreak', 'date_of_outbreak']

class StateStayInPlaceSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state')

    class Meta:
        model = StayInPlace
        fields = ['state', 'order', 'date']

class StateSchoolClosureSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state')

    class Meta:
        model = SchoolClosure
        fields = ['state', 'order', 'date']

class StateDailyFlightsSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state')

    class Meta:
        model = DailyFlights
        fields = ['state', 'date', 'number_of_inbound_flights', 'number_of_outbound_flights']

class StateDemographicsSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state')

    class Meta:
        model = Demographics
        fields = ['state', 'population', 'population_density', 'percent_male', 'percent_female', 'median_age', 'percent_60s', 'percent_70s', 'percent_80_plus']

class CountyDemographicsSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.county.parent_region')
    county = serializers.StringRelatedField(source='region.county')

    class Meta:
        model = Demographics
        fields = ['state', 'county', 'population', 'population_density', 'percent_male', 'percent_female', 'median_age', 'percent_60s', 'percent_70s', 'percent_80_plus']

class StateDailyWeatherSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state')

    class Meta:
        model = DailyWeather
        fields = ['state', 'date', 'avg_temperature', 'max_temperature', 'min_temperature', 'avg_humidity', 'uv_index']

# TODO: Weather serializer
# TODO: Demographics serializer
# TODO: Update all state and county serializers for new regions models
# Future release: County Serializer