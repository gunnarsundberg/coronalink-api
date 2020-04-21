from django.db import models

#
# Section: Base Models
#

class Country(models.Model):
    country_name = models.CharField(max_length=20, blank=False)

class State(models.Model):
    state_name = models.CharField(max_length=20, blank=False)
    code = models.CharField(max_length=2)
    fips_code = models.CharField(max_length=2)
    #country = models.ForeignKey(Country)

    def __str__(self):
        return self.code

class County(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    county_name = models.CharField(max_length=25)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timezone_str = models.CharField(max_length=25)
    fips_code = models.CharField(max_length=3)

    def __str__(self):
        return self.county_name

class Healthcare(models.Model):
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

class Airport(models.Model):
    airport_name = models.CharField(max_length = 100)
    icao_code = models.CharField(max_length = 4)
    timezone = models.CharField(max_length = 30)

    def __str__(self):
        return self.airport_name

class WeatherStation(models.Model):
    station_name = models.CharField(max_length= 25)
    station_id = models.CharField(max_length=5)

    def __str__(self):
        return self.station_name

class Demographics(models.Model):
    population = models.IntegerField()
    population_density = models.FloatField()
    percent_men = models.FloatField()
    percent_women = models.FloatField()
    average_age = models.FloatField()
    percent_over_60 = models.FloatField()

class OutbreakCumulative(models.Model):
    date = models.DateField()
    cases = models.IntegerField()
    negative_tests = models.IntegerField(null=True)
    total_tested = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    hospitalized = models.IntegerField(null=True)
    in_icu = models.IntegerField(null=True)

class Outbreak(OutbreakCumulative):
    admitted_to_hospital = models.IntegerField(null=True)

class StayInPlace(models.Model):
    order = models.BooleanField()
    date = models.DateField()

class SchoolClosure(models.Model):
    order = models.BooleanField()
    date = models.DateField()

class DailyFlights(models.Model):
    date = models.DateField()
    number_of_inbound_flights = models.IntegerField()
    number_of_outbound_flights = models.IntegerField()

class DailyWeather(models.Model):
    temperature = models.IntegerField()
    humidity = models.FloatField()
    uv_index = models.FloatField()
    sunlight_duration = models.FloatField()

#
# Section: State models
#

class StateHealthcare(Healthcare):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateAirport(Airport):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateDemographics(Demographics):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateOutbreak(Outbreak):
    state = models.ForeignKey(State, on_delete=models.CASCADE, unique_for_date="date")

    @property
    def date_of_outbreak(self):
        # Return the date of the outbreak object with the earliest date
        return super().objects.filter(state=state).earliest('date').date

    @property
    def days_since_outbreak(self):
        # Return the number of days since outbreak
        return self.date - self.date_of_outbreak

class StateOutbreakCumulative(OutbreakCumulative):
    state = models.ForeignKey(State, on_delete=models.CASCADE, unique_for_date="date")

    @property
    def date_of_outbreak(self):
        # Return the date of the outbreak object with the earliest date
        return super().objects.filter(state=state).earliest('date').date

class StateStayInPlace(StayInPlace):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateSchoolClosure(SchoolClosure):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateDailyFlights(DailyFlights):
    state = models.ForeignKey(State, on_delete=models.CASCADE, unique_for_date="date")

class StateDailyWeather(DailyWeather):
    state = models.ForeignKey(State, on_delete=models.CASCADE, unique_for_date="date")

#
# Section: County Models
#

class CountyHealthcare(Healthcare):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountyDemographics(Demographics):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountyOutbreak(Outbreak):
    county = models.ForeignKey(County, on_delete=models.CASCADE, unique_for_date="date")

class CountyOutbreakCumulative(OutbreakCumulative):
    county = models.ForeignKey(County, on_delete=models.CASCADE, unique_for_date="date")

class CountyStayInPlace(StayInPlace):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountySchoolClosure(SchoolClosure):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountyDailyWeather(DailyWeather):
    county = models.ForeignKey(County, on_delete=models.CASCADE, unique_for_date="date")

# Meteostat API requires getting weather by station. UV Index is separate and is called by coordinates
class CountyWeatherStation(WeatherStation):
    county = models.ForeignKey(County, on_delete=models.CASCADE)