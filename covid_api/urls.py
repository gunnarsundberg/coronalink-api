from django.urls import path
from rest_framework import routers
from django.conf.urls import url
from covid_api.views import StateOutbreakView, StateOutbreakCumulativeView, StateOutbreakCumulativeHistoricView, StateStayInPlaceView, StateSchoolClosureView, StateDailyFlightsView, StateDemographicsView, CountyDemographicsView, StateDailyWeatherView, CountyDailyWeatherView, StateView
from rest_framework_cache.registry import cache_registry

cache_registry.autodiscover()

urlpatterns = [
    # TODO: States URL, Demographics URL, Medical URL
    url(r'v1/outbreak/daily/states', StateOutbreakView.as_view()),
    url(r'v1/outbreak/cumulative/states', StateOutbreakCumulativeView.as_view()),
    url(r'v1/outbreak/cumulative/historic/states', StateOutbreakCumulativeHistoricView.as_view()),
    
    # Distancing
    url(r'v1/distancing/stayinplace/states', StateStayInPlaceView.as_view()),
    url(r'v1/distancing/schoolclosure/states', StateSchoolClosureView.as_view()),

    # Flights
    url(r'v1/flights/daily/states', StateDailyFlightsView.as_view()),

    # Weather
    url(r'v1/weather/daily/states', StateDailyWeatherView.as_view()),
    #url(r'v1/weather/daily/counties', CountyDailyWeatherView.as_view()),

    # Demographics
    url(r'v1/demographics/states', StateDemographicsView.as_view()),
    #url(r'v1/demographics/counties', CountyDemographicsView.as_view()),

    # Regions
    url(r'v1/regions/states', StateView.as_view()),
]