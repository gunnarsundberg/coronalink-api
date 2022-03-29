from django.urls import re_path
from rest_framework import routers
from covid_api.views import StateCasesView, CountyCasesView, StateTestsView, StateView, CountyView

urlpatterns = [
    re_path(r'cases/states', StateCasesView.as_view()),
    re_path(r'cases/counties', CountyCasesView.as_view()),

    re_path(r'tests/states', StateTestsView.as_view()),

    # Regions
    re_path(r'regions/states', StateView.as_view()),
    re_path(r'regions/counties', CountyView.as_view())
]