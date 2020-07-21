from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import permissions
import django_filters
from covid_data.models import Region, State, County, Outbreak, OutbreakCumulative, DailyFlights, Demographics, DailyWeather, DisplayDate
from covid_api.serializers import StateSerializer, StateOutbreakSerializer, StateOutbreakCumulativeSerializer, StateDailyFlightsSerializer, StateDemographicsSerializer, CountyDemographicsSerializer, StateDailyWeatherSerializer, CountyDailyWeatherSerializer

"""
Section: foreign key filters
Allows looking up states by code through URL query params rather than PK
Must be a filter for every model that will be filtered by state
"""

class StateOutbreakFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region__state',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = Outbreak
        fields = ('state', 'date',)

class StateOutbreakCumulativeFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region__state',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = OutbreakCumulative
        fields = ('state', 'date',)

"""
class StateStayInPlaceFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region__state',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = StayInPlace
        fields = ('state', 'date',)

class StateSchoolClosureFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region__state',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = SchoolClosure
        fields = ('state', 'date',)
"""

class StateDailyFlightsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region__state',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = DailyFlights
        fields = ('state', 'date',)

class StateDemographicsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region__state',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = Demographics
        fields = ('state',)

# TODO: Daily weather filter classes

#
# Section: DRF views
#

class StateOutbreakView(ListAPIView):
    """
    API endpoint that daily outbreak numbers to be viewed.
    """
    serializer_class = StateOutbreakSerializer
    filter_class = StateOutbreakFilter
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Outbreak.objects.filter(region__in=State.objects.all()).filter(date__lte=DisplayDate.objects.all().latest('date').date).order_by('-date','region')
        return queryset

class StateOutbreakCumulativeView(ListAPIView):
    """
    API endpoint that allows cumulative outbreak numbers to be viewed.
    """
    serializer_class = StateOutbreakCumulativeSerializer
    filter_class = StateOutbreakCumulativeFilter
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = OutbreakCumulative.objects.filter(region__in=State.objects.all()).filter(date=DisplayDate.objects.all().latest('date').date).order_by('region')
        return queryset
    
class StateOutbreakCumulativeHistoricView(ListAPIView):
    """
    API endpoint that allows historic cumulative outbreak numbers to be viewed.
    """
    serializer_class = StateOutbreakCumulativeSerializer
    filter_class = StateOutbreakCumulativeFilter
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = OutbreakCumulative.objects.filter(region__in=State.objects.all()).filter(date__lte=DisplayDate.objects.all().latest('date').date).order_by('-date','region')
        return queryset
"""
class StateStayInPlaceView(ListAPIView):
    
    API endpoint that allows statewide stay in place orders to be viewed.

    serializer_class = StateStayInPlaceSerializer
    filter_class = StateStayInPlaceFilter
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = StayInPlace.objects.filter(region__in=State.objects.all()).order_by('region')
        return queryset

class StateSchoolClosureView(ListAPIView):
    
    API endpoint that allows statewide school closures to be viewed.
    
    serializer_class = StateSchoolClosureSerializer
    filter_class = StateSchoolClosureFilter
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = SchoolClosure.objects.filter(region__in=State.objects.all()).order_by('region')
        return queryset
"""

class StateDailyFlightsView(ListAPIView):
    """
    API endpoint that allows state inbound and outbound flights to viewed.
    """
    serializer_class = StateDailyFlightsSerializer
    filter_class = StateDailyFlightsFilter
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = DailyFlights.objects.filter(region__in=State.objects.all()).filter(date__lte=DisplayDate.objects.all().latest('date').date).order_by('-date','region')
        return queryset

class StateDemographicsView(ListAPIView):
    """
    API endpoint that lists state demographics
    """
    queryset = Demographics.objects.filter(region__in=State.objects.all())
    serializer_class = StateDemographicsSerializer
    filter_class = StateDemographicsFilter

class CountyDemographicsView(ListAPIView):
    """
    API endpoint that lists state demographics
    """
    queryset = Demographics.objects.filter(region__in=County.objects.all())
    serializer_class = CountyDemographicsSerializer

class StateDailyWeatherView(ListAPIView):
    """
    API endpoint listing daily weather by state. All values are averages of county values, including max and mins.
    """
    serializer_class = StateDailyWeatherSerializer

    def get_queryset(self):
        queryset = DailyWeather.objects.filter(region__in=State.objects.all()).filter(date__lte=DisplayDate.objects.all().latest('date').date).order_by('-date','region')
        return queryset

class CountyDailyWeatherView(ListAPIView):
    """
    API endpoint listing daily weather by county.
    """
    serializer_class = CountyDailyWeatherSerializer

    def get_queryset(self):
        queryset = DailyWeather.objects.filter(region__in=County.objects.all()).filter(date__lte=DisplayDate.objects.all().latest('date').date)
        return queryset

class StateView(ListAPIView):
    """
    API endpoint that lists state-type regions (USA States)
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer

# TODO: Weather view
# TODO: Demographics view
    
# Future release: County view
