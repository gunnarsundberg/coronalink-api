from django.db import models
#from django_prometheus.models import ExportModelOperationsMixin

# Note: Commented class definitions will be used when django_prometheus integration is ready

"""
Section: Base Models
"""
class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Future Release
#class Country(models.Model):
#    name = models.CharField(max_length=20, blank=False)
#    region = models.ForeignKey(Region, on_delete=models.CASCADE)

#class DisplayDate(ExportModelOperationsMixin('displaydate'), models.Model):
class DisplayDate(models.Model):
    date = models.DateField()

#class State(ExportModelOperationsMixin('State'), Region):
class State(Region):
    code = models.CharField(max_length=2)
    fips_code = models.CharField(max_length=2)
    #update_timezone = models.CharField(max_length=25)
    land_area = models.FloatField()
    #parent_region = models.ForeignKey(Country)

    def __str__(self):
        return self.code

#class County(ExportModelOperationsMixin('County'), Region):
class County(Region):
    parent_region = models.ForeignKey(State, on_delete=models.CASCADE)
    fips_code = models.CharField(max_length=5)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timezone_str = models.CharField(max_length=35)
    land_area = models.FloatField()

    def __str__(self):
        return self.name

#class Healthcare(ExportModelOperationsMixin('Healthcare'), models.Model):
class Healthcare(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    number_of_hospital_beds = models.IntegerField()
    number_of_icu_beds = models.IntegerField()
    number_of_er_doctors = models.IntegerField()
    number_of_er_nurses = models.IntegerField()
    percent_heart_disease = models.FloatField()
    percent_lung_disease = models.FloatField()

    @property
    def hospital_beds_per_capita(self):
        pass

    @property
    def icu_beds_per_capita(self):
        pass

#class Airport(ExportModelOperationsMixin('Airport'), models.Model):
class Airport(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    airport_name = models.CharField(max_length = 100)
    icao_code = models.CharField(max_length = 4)
    timezone = models.CharField(max_length = 30)

    def __str__(self):
        return self.airport_name

"""
class WeatherStation(models.Model):
    station_name = models.CharField(max_length= 25)
    station_id = models.CharField(max_length=5)

    def __str__(self):
        return self.station_name
"""

#class Demographics(ExportModelOperationsMixin('Demographics'), models.Model):
class Demographics(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    population = models.IntegerField()
    population_density = models.FloatField()
    percent_male = models.FloatField()
    percent_female = models.FloatField()
    median_age = models.FloatField()
    percent_60s = models.FloatField()
    percent_70s = models.FloatField()
    percent_80_plus = models.FloatField()

#class OutbreakCumulative(ExportModelOperationsMixin('Outbreak Cumulative'), models.Model):
class OutbreakCumulative(models.Model):
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    cases = models.IntegerField()
    negative_tests = models.IntegerField(null=True)
    total_tested = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    hospitalized = models.IntegerField(null=True)
    in_icu = models.IntegerField(null=True)
    date_of_outbreak = models.DateField()
    days_since_outbreak = models.IntegerField()

    unique_together = ['date', 'region']

    def save(self, *args, **kwargs):
        # Check if there are existing outbreaks for this state
        if OutbreakCumulative.objects.filter(region=self.region).exists():
            # Use the date of the outbreak object with the earliest date
            self.date_of_outbreak = OutbreakCumulative.objects.filter(region=self.region).earliest('date').date
        else:
            self.date_of_outbreak = self.date
        
        self.days_since_outbreak = (self.date - self.date_of_outbreak).days

        super().save(*args, **kwargs)

#class Outbreak(ExportModelOperationsMixin('Outbreak'), OutbreakCumulative):
class Outbreak(models.Model):
    admitted_to_hospital = models.IntegerField(null=True)
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    cases = models.IntegerField()
    negative_tests = models.IntegerField(null=True)
    total_tested = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    hospitalized = models.IntegerField(null=True)
    in_icu = models.IntegerField(null=True)
    date_of_outbreak = models.DateField()
    days_since_outbreak = models.IntegerField()

    unique_together = ['date', 'region']

    def save(self, *args, **kwargs):
        # Check if there are existing outbreaks for this state
        if OutbreakCumulative.objects.filter(region=self.region).exists():
            # Use the date of the outbreak object with the earliest date
            self.date_of_outbreak = OutbreakCumulative.objects.filter(region=self.region).earliest('date').date
        else:
            self.date_of_outbreak = self.date
        
        self.days_since_outbreak = (self.date - self.date_of_outbreak).days

        super().save(*args, **kwargs)

#class StayInPlace(ExportModelOperationsMixin('Stay In Place Order'), models.Model):
class StayInPlace(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    order = models.BooleanField()
    date = models.DateField()

#class SchoolClosure(ExportModelOperationsMixin('School Closure'), models.Model):
class SchoolClosure(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    order = models.BooleanField()
    date = models.DateField()

#class DailyFlights(ExportModelOperationsMixin('Daily Flights'), models.Model):
class DailyFlights(models.Model):
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    number_of_inbound_flights = models.IntegerField()
    number_of_outbound_flights = models.IntegerField()

    unique_together = ['date', 'region']

#class DailyWeather(ExportModelOperationsMixin('Daily Weather'), models.Model):
class DailyWeather(models.Model):
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    avg_temperature = models.IntegerField()
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    avg_humidity = models.FloatField()
    uv_index = models.FloatField()

    unique_together = ['date', 'region']

"""
# Meteostat API requires getting weather by station. UV Index is separate and is called by coordinates
class CountyWeatherStation(WeatherStation):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
"""