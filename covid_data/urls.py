from django.urls import path
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from covid_data.views import download_county_data

admin.site.site_header = 'Poly COVID Project Administration'
admin.site.site_title = 'Poly COVID Project'

urlpatterns = [
    url(r'downloads/countydata', download_county_data),
]
