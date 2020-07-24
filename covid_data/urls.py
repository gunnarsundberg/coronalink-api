from django.urls import path
from django.conf.urls import url
from covid_data.views import download_county_data



urlpatterns = [
    url(r'downloads/countydata', download_county_data),
]
