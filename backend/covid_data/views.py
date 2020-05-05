from django.shortcuts import render
from rest_framework.generics import ListAPIView
#from rest_framework import viewsets
from rest_framework import permissions
import django_filters
from covid_data.models import State, StateOutbreak, StateOutbreakCumulative, StateStayInPlace, StateSchoolClosure, StateDailyFlights
from covid_data.serializers import StateSerializer, StateOutbreakSerializer, StateOutbreakCumulativeSerializer, StateStayInPlaceSerializer, StateSchoolClosureSerializer, StateDailyFlightsSerializer

#
# Section: foreign key filters
# Allows looking up states by code through URL query params rather than PK
# Must be a filter for every model that will be filtered by state
#

class StateOutbreakFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='state__code',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = StateOutbreak
        fields = ('state', 'date',)

class StateOutbreakCumulativeFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='state__code',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = StateOutbreakCumulative
        fields = ('state', 'date',)

class StateStayInPlaceFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='state__code',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = StateStayInPlace
        fields = ('state', 'date',)

class StateSchoolClosureFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='state__code',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = StateSchoolClosure
        fields = ('state', 'date',)

class StateDailyFlightsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(field_name='state__code',
                                            to_field_name='code',
                                            queryset=State.objects.all())

    class Meta:
        model = StateDailyFlights
        fields = ('state', 'date', 'number_of_inbound_flights', 'number_of_outbound_flights')

#
# Section: DRF views
#

class StateOutbreakView(ListAPIView):
    """
    API endpoint that daily outbreak numbers to be viewed.
    """
    queryset = StateOutbreak.objects.all().order_by('-date','state')
    serializer_class = StateOutbreakSerializer
    filter_class = StateOutbreakFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateOutbreakCumulativeView(ListAPIView):
    """
    API endpoint that allows cumulative outbreak numbers to be viewed.
    """
    latest = StateOutbreakCumulative.objects.latest('date').date
    queryset = StateOutbreakCumulative.objects.filter(date=latest)
    serializer_class = StateOutbreakCumulativeSerializer
    filter_class = StateOutbreakCumulativeFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateOutbreakCumulativeHistoricView(ListAPIView):
    """
    API endpoint that allows historic cumulative outbreak numbers to be viewed.
    """
    queryset = StateOutbreakCumulative.objects.all().order_by('-date','state')
    serializer_class = StateOutbreakCumulativeSerializer
    filter_class = StateOutbreakCumulativeFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateStayInPlaceView(ListAPIView):
    """
    API endpoint that allows statewide stay in place orders to be viewed.
    """
    queryset = StateStayInPlace.objects.all().order_by('state')
    serializer_class = StateStayInPlaceSerializer
    filter_class = StateStayInPlaceFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateSchoolClosureView(ListAPIView):
    """
    API endpoint that allows statewide school closures to be viewed.
    """
    queryset = StateSchoolClosure.objects.all().order_by('state')
    serializer_class = StateSchoolClosureSerializer
    filter_class = StateSchoolClosureFilter
    #permission_classes = [permissions.IsAuthenticated]

class StateDailyFlightsView(ListAPIView):
    """
    API endpoint that allows state inbound and outbound flights to viewed.
    """
    queryset = StateDailyFlights.objects.all().order_by('-date','state__state_name')
    serializer_class = StateDailyFlightsSerializer
    filter_class = StateDailyFlightsFilter
    #permission_classes = [permissions.IsAuthenticated]