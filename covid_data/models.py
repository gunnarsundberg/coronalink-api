from django.db import models
import pandas as pd
#from django_prometheus.models import ExportModelOperationsMixin

# Note: Commented class definitions will be used when django_prometheus integration is ready
"""
Section: Model Mixins
"""
class PandasModelMixin(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def as_dataframe(cls, queryset=None, field_list=None):
        if queryset is None:
            queryset = cls.objects.all()
        if field_list is None:
            field_list = [_field.name for _field in cls._meta._get_fields(reverse=False)]

        data = []
        [data.append([obj.serializable_value(column) for column in field_list]) for obj in queryset]

        columns = field_list

        df = pd.DataFrame(data, columns=columns)
        return df

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

class RegionAdjacency(PandasModelMixin):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    adjacent_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="neighbor")

    # Baseline number of people commuting to adjacent region from region, as measure of connectivity
    edge_weight = models.IntegerField(null=True)

#class Healthcare(ExportModelOperationsMixin('Healthcare'), models.Model):
class Healthcare(PandasModelMixin):
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

#class Demographics(ExportModelOperationsMixin('Demographics'), models.Model):
class Demographics(PandasModelMixin):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    population = models.IntegerField()
    population_density = models.FloatField()
    percent_male = models.FloatField()
    percent_female = models.FloatField()
    median_age = models.FloatField()
    percent_60s = models.FloatField()
    percent_70s = models.FloatField()
    percent_80_plus = models.FloatField()
    total_poverty = models.IntegerField(null=True)
    percent_poverty = models.FloatField(null=True)

class CountyUrbanRelation(PandasModelMixin):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    """
    Rural-Urban Continuum Codes
    """
    METRO_GT_1MIL = '1'
    METRO_250K_1MIL = '2'
    METRO_LT_250K = '3'
    URB_GT_20K_ADJ = '4'
    URB_GT_20K_NADJ = '5'
    URB_LT_20K_ADJ = '6'
    URB_LT_20K_NADJ = '7'
    LT_2K_ADJ = '8'
    LT_2K_NADJ = '9'

    CONTINUUM_CHOICES = [
        (METRO_GT_1MIL, 'Counties in metro areas of 1 million population or more'),
        (METRO_250K_1MIL, 'Counties in metro areas of 250,000 to 1 million population'),
        (METRO_LT_250K, 'Counties in metro areas of fewer than 250,000 population'),
        (URB_GT_20K_ADJ, 'Urban population of 20,000 or more, adjacent to a metro area'),
        (URB_GT_20K_NADJ, 'Urban population of 20,000 or more, not adjacent to a metro area'),
        (URB_LT_20K_ADJ, 'Urban population of 2,500 to 19,999, adjacent to a metro area'),
        (URB_LT_20K_NADJ, 'Urban population of 2,500 to 19,999, not adjacent to a metro area'),
        (LT_2K_ADJ, 'Completely rural or less than 2,500 urban population, adjacent to a metro area'),
        (LT_2K_NADJ, 'Completely rural or less than 2,500 urban population, not adjacent to a metro area')
    ]

    """
    Urban Influence Codes
    """
    METRO_GT_1MIL = '1'
    METRO_LT_1MIL = '2'
    M_ADJ_LM = '3'
    NC_ADJ_LM = '4'
    M_ADJ_SM = '5'
    NC_ADJ_SM_GT_2K = '6'
    NC_ADJ_SM_LT_2K = '7'
    M_NADJ_METRO = '8'
    NC_ADJ_M_GT_2K = '9'
    NC_ADJ_M_LT_2K = '10'
    NC_NADJ_M_GT_2K = '11'
    NC_NADJ_M_LT_2K = '12'

    INFLUENCE_CHOICES = [
        (METRO_GT_1MIL, 'In large metro area of 1+ million residents'),
        (METRO_LT_1MIL, 'In small metro area of less than 1 million residents'),
        (M_ADJ_LM, 'Micropolitan area adjacent to large metro area'),
        (NC_ADJ_LM, 'Noncore adjacent to large metro area'),
        (M_ADJ_SM, 'Micropolitan area adjacent to small metro area'),
        (NC_ADJ_SM_GT_2K, 'Noncore adjacent to small metro area and contains a town of at least 2,500 residents'),
        (NC_ADJ_SM_LT_2K, 'Noncore adjacent to small metro area and does not contain a town of at least 2,500 residents'),
        (M_NADJ_METRO, 'Micropolitan area not adjacent to a metro area'),
        (NC_ADJ_M_GT_2K, 'Noncore adjacent to micro area and contains a town of at least 2,500 residents'),
        (NC_ADJ_M_LT_2K, 'Noncore adjacent to micro area and does not contain a town of at least 2,500 residents'),
        (NC_NADJ_M_GT_2K, 'Noncore not adjacent to metro or micro area and contains a town of at least 2,500 residents'),
        (NC_NADJ_M_LT_2K, 'Noncore not adjacent to metro or micro area and does not contain a town of at least 2,500 residents')
    ]

    urban_continuum_code = models.CharField(max_length=1, choices=CONTINUUM_CHOICES)
    urban_influence_code = models.CharField(max_length=2, choices=INFLUENCE_CHOICES)

#class OutbreakCumulative(ExportModelOperationsMixin('Outbreak Cumulative'), models.Model):
class OutbreakCumulative(PandasModelMixin):
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
class Outbreak(PandasModelMixin):
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
    # (Cases * commuter flow)/(number of people staying home) summed for all surrounding counties
    case_adjacency_risk = models.FloatField(null=True)

    unique_together = ['date', 'region']

    def get_adjacency_risk(self):
        if RegionAdjacency.objects.filter(region=self.region).exists():
            total_adjacency_risk = 0
            adjacent_regions = RegionAdjacency.objects.filter(region=self.region)
            for adjacency_record in adjacent_regions:
                try:
                    adjacent_cases = Outbreak.objects.filter(region=adjacency_record.adjacent_region).get(date=self.date).cases
                    if adjacent_cases > 0:
                        record_risk = adjacent_cases
                    else:
                        adjacent_cases = 0
                    record_risk *= adjacency_record.edge_weight
                    population_at_home = DailyTrips.objects.filter(date=self.date).get(region=self.region).population_at_home
                    if population_at_home > 0:
                        record_risk /= population_at_home
                    total_adjacency_risk += record_risk
                except:
                    continue
            self.case_adjacency_risk = round(total_adjacency_risk, ndigits=1)
            self.save()
        else:
            self.case_adjacency_risk = 0
            self.save()

    def save(self, *args, **kwargs):
        # Check if there are existing outbreaks for this state
        if OutbreakCumulative.objects.filter(region=self.region).exists():
            # Use the date of the outbreak object with the earliest date
            self.date_of_outbreak = OutbreakCumulative.objects.filter(region=self.region).earliest('date').date
        else:
            self.date_of_outbreak = self.date
        
        self.days_since_outbreak = (self.date - self.date_of_outbreak).days

        super().save(*args, **kwargs)

class DistancingPolicy(PandasModelMixin):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    date = models.DateField()

    """
    Order Type
    """
    STAY_AT_HOME = '0'
    GATHERINGS_50 = '1'
    GATHERINGS_500 = '2'
    SCHOOL_CLOSURE = '3'
    DINE_IN = '4'
    ENTERTAINMENT_GYM = '5'

    ORDER_CHOICES = [
        (STAY_AT_HOME, 'Stay At Home Order'),
        (GATHERINGS_50, 'Gatherings >50'),
        (GATHERINGS_500, 'Gatherings >500'),
        (SCHOOL_CLOSURE, 'Public School Closure'),
        (DINE_IN, 'Restaurant Dine-In'),
        (ENTERTAINMENT_GYM, 'Entertainment/Gym'),
    ]

    order_type = models.CharField(max_length=1, choices=ORDER_CHOICES)

class DistancingPolicyRollback(PandasModelMixin):
    policy = models.ForeignKey(DistancingPolicy, on_delete=models.CASCADE)
    date = models.DateField()

    unique_together = ['policy', 'date']

class MobilityTrends(PandasModelMixin):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    date = models.DateField()

    retail_and_recreation_trend = models.FloatField(null=True)
    grocery_and_pharmacy_trend = models.FloatField(null=True)
    parks_trend = models.FloatField(null=True)
    transit_trend = models.FloatField(null=True)
    workplace_trend = models.FloatField(null=True)
    residential_trend = models.FloatField(null=True)

    unique_together = ['region', 'date']

class DailyTrips(PandasModelMixin):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    date = models.DateField()

    population_at_home = models.IntegerField()
    population_out_of_home = models.IntegerField()
    total_trips = models.IntegerField()
    trips_lt_1 = models.IntegerField()
    trips_1_3 = models.IntegerField()
    trips_3_5 = models.IntegerField()
    trips_5_10 = models.IntegerField()
    trips_10_25 = models.IntegerField()
    trips_25_50 = models.IntegerField()
    trips_50_100 = models.IntegerField()
    trips_100_250 = models.IntegerField()
    trips_250_500 = models.IntegerField()
    trips_gt_500 = models.IntegerField()

    unique_together = ['region', 'date']

#class DailyFlights(ExportModelOperationsMixin('Daily Flights'), models.Model):
class DailyFlights(PandasModelMixin):
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    number_of_inbound_flights = models.IntegerField()
    number_of_outbound_flights = models.IntegerField()

    unique_together = ['date', 'region']

#class DailyWeather(ExportModelOperationsMixin('Daily Weather'), models.Model):
class DailyWeather(PandasModelMixin):
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    avg_temperature = models.FloatField()
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    avg_humidity = models.FloatField()
    uv_index = models.FloatField()

    unique_together = ['date', 'region']