from rest_framework.generics import ListAPIView, ListCreateAPIView
from covid_api.permissions import IsStaffOrReadOnly
from covid_api.models import State, County, RegionalCases, RegionalTests
from covid_api.serializers import StateSerializer, CountySerializer
from covid_api.serializers import StateCasesSerializer, CountyCasesSerializer
from covid_api.serializers import StateTestsSerializer
from covid_api.filters import CountyFilter, StateCasesFilter, CountyCasesFilter

class StateView(ListCreateAPIView):
    """
    API endpoint that lists state-type regions (USA States)
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = (IsStaffOrReadOnly,)

class CountyView(ListCreateAPIView):
    """
    API endpoint that lists county-type regions (USA Counties)
    """
    queryset = County.objects.all()
    serializer_class = CountySerializer
    filter_class = CountyFilter
    permission_classes = (IsStaffOrReadOnly,)

class StateCasesView(ListAPIView):
    """
    API endpoint that daily outbreak numbers to be viewed.
    """
    serializer_class = StateCasesSerializer
    filter_class = StateCasesFilter
    permission_classes = (IsStaffOrReadOnly,)

    def get_queryset(self):
        queryset = RegionalCases.objects.filter(region__in=State.objects.all()).order_by('-date','region')
        return queryset

class CountyCasesView(ListAPIView):
    """
    API endpoint that daily outbreak numbers to be viewed.
    """
    serializer_class = CountyCasesSerializer
    filter_class = CountyCasesFilter
    permission_classes = (IsStaffOrReadOnly,)

    def get_queryset(self):
        queryset = RegionalCases.objects.filter(region__in=County.objects.all()).order_by('-date','region')
        return queryset

class StateTestsView(ListAPIView):
    """
    API endpoint that lists daily test data.
    """
    serializer_class = StateTestsSerializer
    #filter_class = StateCasesFilter
    permission_classes = (IsStaffOrReadOnly,)

    def get_queryset(self):
        queryset = RegionalTests.objects.filter(region__in=State.objects.all()).order_by('-date','region')
        return queryset
