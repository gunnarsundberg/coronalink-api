from django.db import models

# Section: Base Models

class Country(models.Model):
    country_name = models.CharField(max_length=20, blank=False)

class State(models.Model):
    state_name = models.CharField(max_length=20, blank=False)
    code = models.CharField(max_length=2)
    fips_code = models.CharField(max_length=2)
    #country = models.ForeignKey(Country)

class County(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    county_name = models.CharField(max_length=25)
    latitude = models.FloatField()
    longitude = models.FloatField()
    fips_code = models.CharField(max_length=3)

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

class WeatherStation(models.Model):
    station_name = models.CharField(max_length= 25)
    station_id = models.CharField(max_length=5)

class Demographics(models.Model):
    population = models.IntegerField()
    population_density = models.FloatField()
    percent_men = models.FloatField()
    percent_women = models.FloatField()
    average_age = models.FloatField()
    percent_over_60 = models.FloatField()

class OutbreakCumulative(models.Model):
    date = models.DateField()
    cases = models.IntegerField(blank=False)
    negative_tests = models.IntegerField()
    total_tested = models.IntegerField()
    deaths = models.IntegerField()
    hospitalized = models.IntegerField()
    in_icu = models.IntegerField()

    @property
    def start_date(self):
        try:
            # Return the date of the outbreak object with the earliest date
            return super().objects.order_by('date')[0].date
        except:
            print("Error. No outbreak objects have been created yet.")

class Outbreak(OutbreakCumulative):
    admitted_to_hospital = models.IntegerField()

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
    sunlight_direction = models.FloatField()

# Section: State models

class StateHealthcare(Healthcare):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateAirport(Airport):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateDemographics(Demographics):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateOutbreak(Outbreak):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateOutbreakCumulative(OutbreakCumulative):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateStayInPlace(StayInPlace):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateSchoolClosure(SchoolClosure):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateDailyFlights(DailyFlights):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class StateDailyWeather(DailyWeather):
    state = models.ForeignKey(State, on_delete=models.CASCADE)

# Section: County Models

class CountyHealthcare(Healthcare):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountyDemographics(Demographics):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountyOutbreak(Outbreak):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountyOutbreakCumulative(OutbreakCumulative):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountyStayInPlace(StayInPlace):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountySchoolClosure(SchoolClosure):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

class CountyDailyWeather(DailyWeather):
    county = models.ForeignKey(County, on_delete=models.CASCADE)