from django.urls import path
from rest_framework import routers
from django.conf.urls import url
from django.urls import include
from covid_data.views import StateOutbreakView, StateOutbreakCumulativeView, StateOutbreakCumulativeHistoricView, StateStayInPlaceView, StateSchoolClosureView, StateDailyFlightsView


urlpatterns = [
    # TODO: States URL, Demographics URL, Medical URL
    url(r'v1/outbreak/daily/states', StateOutbreakView.as_view()),
    url(r'v1/outbreak/cumulative/states', StateOutbreakCumulativeView.as_view()),
    url(r'v1/outbreak/cumulative/historic/states', StateOutbreakCumulativeHistoricView.as_view()),
    url(r'v1/stayinplace/states', StateStayInPlaceView.as_view()),
    url(r'v1/schoolclosure/states', StateSchoolClosureView.as_view()),
    url(r'v1/flights/daily/states', StateDailyFlightsView.as_view())
]
