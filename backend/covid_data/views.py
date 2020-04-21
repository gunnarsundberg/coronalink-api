from django.shortcuts import render
from rest_framework.generics import ListAPIView
#from rest_framework import viewsets
from rest_framework import permissions
from covid_data.models import StateOutbreak, StateOutbreakCumulative, StateStayInPlace, StateSchoolClosure, StateDailyFlights
from covid_data.serializers import StateOutbreakSerializer, StateOutbreakCumulativeSerializer, StateStayInPlaceSerializer, StateSchoolClosureSerializer, StateDailyFlightsSerializer


class StateOutbreakView(ListAPIView):
    """
    API endpoint that daily outbreak numbers to be viewed.
    """
    queryset = StateOutbreak.objects.all().order_by('-date','state')
    serializer_class = StateOutbreakSerializer
    #permission_classes = [permissions.IsAuthenticated]

class StateOutbreakCumulativeView(ListAPIView):
    """
    API endpoint that allows cumulative outbreak numbers to be viewed.
    """
    latest = StateOutbreakCumulative.objects.latest('date').date
    queryset = StateOutbreakCumulative.objects.filter(date=latest)
    serializer_class = StateOutbreakCumulativeSerializer
    #permission_classes = [permissions.IsAuthenticated]

class StateOutbreakCumulativeHistoricView(ListAPIView):
    """
    API endpoint that allows historic cumulative outbreak numbers to be viewed.
    """
    queryset = (StateOutbreakCumulative.objects.all()).order_by('-date','state')
    serializer_class = StateOutbreakCumulativeSerializer
    #permission_classes = [permissions.IsAuthenticated]

class StateStayInPlaceView(ListAPIView):
    """
    API endpoint that allows statewide stay in place orders to be viewed.
    """
    queryset = StateStayInPlace.objects.all().order_by('state')
    serializer_class = StateStayInPlaceSerializer
    #permission_classes = [permissions.IsAuthenticated]

class StateSchoolClosureView(ListAPIView):
    """
    API endpoint that allows statewide school closures to be viewed.
    """
    queryset = StateSchoolClosure.objects.all().order_by('state')
    serializer_class = StateSchoolClosureSerializer
    #permission_classes = [permissions.IsAuthenticated]

class StateDailyFlightsView(ListAPIView):
    """
    API endpoint that allows state inbound and outbound flights to viewed.
    """
    queryset = StateDailyFlights.objects.all().order_by('state')
    serializer_class = StateDailyFlightsSerializer
    #permission_classes = [permissions.IsAuthenticated]