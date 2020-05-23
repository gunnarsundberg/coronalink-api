from django.shortcuts import render
from rest_framework.generics import ListAPIView
#from rest_framework import viewsets
from rest_framework import permissions
import django_filters
from covid_data.models import Region, State, Outbreak, OutbreakCumulative, StayInPlace, SchoolClosure, DailyFlights
from covid_data.serializers import StateSerializer, StateOutbreakSerializer, StateOutbreakCumulativeSerializer, StateStayInPlaceSerializer, StateSchoolClosureSerializer, StateDailyFlightsSerializer

"""
Section: foreign key filters
Allows looking up states by code through URL query params rather than PK
Must be a filter for every model that will be filtered by state
"""

class StateOutbreakFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region',
                                            to_field_name='name',
                                            queryset=Region.objects.filter(state__in=State.objects.all()))

    class Meta:
        model = Outbreak
        fields = ('state', 'date',)

class StateOutbreakCumulativeFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region',
                                            to_field_name='name',
                                            queryset=Region.objects.filter(state__in=State.objects.all()))

    class Meta:
        model = OutbreakCumulative
        fields = ('state', 'date',)

class StateStayInPlaceFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region',
                                            to_field_name='name',
                                            queryset=Region.objects.filter(state__in=State.objects.all()))

    class Meta:
        model = StayInPlace
        fields = ('state', 'date',)

class StateSchoolClosureFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region',
                                            to_field_name='name',
                                            queryset=Region.objects.filter(state__in=State.objects.all()))

    class Meta:
        model = SchoolClosure
        fields = ('state', 'date',)

class StateDailyFlightsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='region',
                                            to_field_name='name',
                                            queryset=Region.objects.filter(state__in=State.objects.all()))

    class Meta:
        model = DailyFlights
        fields = ('state', 'date', 'number_of_inbound_flights', 'number_of_outbound_flights')

#
# Section: DRF views
#

class StateOutbreakView(ListAPIView):
    """
    API endpoint that daily outbreak numbers to be viewed.
    """
    queryset = Outbreak.objects.filter(region__in=State.objects.all()).order_by('-date','region')
    serializer_class = StateOutbreakSerializer
    filter_class = StateOutbreakFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateOutbreakCumulativeView(ListAPIView):
    """
    API endpoint that allows cumulative outbreak numbers to be viewed.
    """
    latest = OutbreakCumulative.objects.filter(region__in=State.objects.all()).latest('date').date
    queryset = OutbreakCumulative.objects.filter(region__in=State.objects.all()).filter(date=latest)
    serializer_class = StateOutbreakCumulativeSerializer
    filter_class = StateOutbreakCumulativeFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateOutbreakCumulativeHistoricView(ListAPIView):
    """
    API endpoint that allows historic cumulative outbreak numbers to be viewed.
    """
    queryset = OutbreakCumulative.objects.filter(region__in=State.objects.all()).order_by('-date','region')
    serializer_class = StateOutbreakCumulativeSerializer
    filter_class = StateOutbreakCumulativeFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateStayInPlaceView(ListAPIView):
    """
    API endpoint that allows statewide stay in place orders to be viewed.
    """
    queryset = StayInPlace.objects.filter(region__in=State.objects.all()).order_by('region')
    serializer_class = StateStayInPlaceSerializer
    filter_class = StateStayInPlaceFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateSchoolClosureView(ListAPIView):
    """
    API endpoint that allows statewide school closures to be viewed.
    """
    queryset = SchoolClosure.objects.filter(region__in=State.objects.all()).order_by('region')
    serializer_class = StateSchoolClosureSerializer
    filter_class = StateSchoolClosureFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateDailyFlightsView(ListAPIView):
    """
    API endpoint that allows state inbound and outbound flights to viewed.
    """
    queryset = DailyFlights.objects.filter(region__in=State.objects.all()).order_by('-date','region')
    serializer_class = StateDailyFlightsSerializer
    filter_class = StateDailyFlightsFilter
    #permission_classes = [permissions.IsAuthenticated]

# TODO: Weather view
# TODO: Demographics view
# TODO: Update all state and county views for new regions models
    
# Future release: County view