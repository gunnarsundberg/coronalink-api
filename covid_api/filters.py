import django_filters
from covid_api.models import State, County, RegionalCases

class CountyFilter(django_filters.FilterSet):
    """
    Allows looking up states by code through URL query params rather than PK
    Must be a filter for every model that will be filtered by state
    """
    state = django_filters.ModelChoiceFilter(
        field_name='parent_region',
        to_field_name='code',
        queryset=State.objects.all()
    )

    class Meta:
        model = County
        fields = ('state', 'fips_code', 'name')

class StateCasesFilter(django_filters.FilterSet):
    """
    Allows looking up states by code through URL query params rather than PK
    Must be a filter for every model that will be filtered by state
    """
    state = django_filters.ModelChoiceFilter(field_name='region__state',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = RegionalCases
        fields = ('state', 'date',)

class CountyCasesFilter(django_filters.FilterSet):
    """
    Allows looking up states by code through URL query params rather than PK
    Must be a filter for every model that will be filtered by state
    """
    state = django_filters.ModelChoiceFilter(
        field_name='region__county__parent_region',
        to_field_name='code',
        queryset=State.objects.all()
    )
    fips_code = django_filters.ModelChoiceFilter(
        field_name='region__county',
        to_field_name='fips_code',
        queryset=County.objects.all()
    )
    name = django_filters.CharFilter(
        field_name='region__name'
    )

    class Meta:
        model = RegionalCases
        fields = ('state', 'fips_code', 'name', 'date')