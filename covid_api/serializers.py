from rest_framework import serializers
from covid_api.models import State, County, RegionalCases, RegionalTests

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['name', 'code', 'fips_code', 'land_area']

class CountySerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='parent_region.code')
    
    def create(self, validated_data):

        state_code = validated_data.pop('state')
        state = State.objects.get(code=state_code)
        parent_region = state
        county = County.objects.create(parent_region=parent_region, **validated_data)
        county.save()

        return county

    class Meta:
        model = County
        fields = ['name', 'state', 'fips_code', 'latitude', 'longitude', 'land_area']

class StateCasesSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state')

    class Meta:
        model = RegionalCases
        fields = [
            'state',
            'date',
            'cumulative_cases',
            'new_cases',
            'cumulative_deaths',
            'new_deaths',
        ]

class CountyCasesSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.county.parent_region.code')
    fips_code = serializers.StringRelatedField(source='region.county.fips_code')
    name = serializers.StringRelatedField(source='region.name')

    class Meta:
        model = RegionalCases
        fields = [
            'name',
            'fips_code',
            'state',
            'date',
            'cumulative_cases',
            'new_cases',
            'cumulative_deaths',
            'new_deaths',
        ]

class StateTestsSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(source='region.state')

    class Meta:
        model = RegionalTests
        fields = [
            'state',
            'date',
            'cumulative_positive',
            'cumulative_negative',
            'cumulative_inconclusive',
            'new_positive',
            'new_negative',
            'new_inconclusive',
        ]