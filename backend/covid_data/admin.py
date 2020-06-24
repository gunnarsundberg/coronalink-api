from django.contrib import admin
from covid_data.models import StayInPlace, SchoolClosure

@admin.register(StayInPlace)
class StayInPlaceAdmin(admin.ModelAdmin):
    list_display = ('region', 'order')
    search_fields = ['region__name']
    date_hierarchy = 'date'
    list_filter = ('order',)
    ordering = ('region', 'order')

@admin.register(SchoolClosure)
class SchoolClosureAdmin(admin.ModelAdmin):
    list_display = ('region', 'order')
    search_fields = ['region__name']
    date_hierarchy = 'date'
    list_filter = ('order',)
    ordering = ('region', 'order')
