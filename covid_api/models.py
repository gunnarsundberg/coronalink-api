from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class State(Region):
    code = models.CharField(max_length=2)
    fips_code = models.CharField(max_length=2)
    land_area = models.FloatField()

    def __str__(self):
        return self.code

class County(Region):
    parent_region = models.ForeignKey(
        State,
        on_delete=models.CASCADE
    )
    fips_code = models.CharField(max_length=5)
    latitude = models.FloatField()
    longitude = models.FloatField()
    land_area = models.FloatField()

    def __str__(self):
        return self.name

class RegionAdjacency(models.Model):
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE
    )
    adjacent_region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="neighbor"
    )

class CountyUrbanRelation(models.Model):
    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE
    )

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
        (
            METRO_GT_1MIL,
            'Counties in metro areas of 1 million population \
                or more'
        ),
        (
            METRO_250K_1MIL,
            'Counties in metro areas of 250,000 to 1 million \
                population'
        ),
        (
            METRO_LT_250K,
            'Counties in metro areas of fewer than 250,000 \
                population'
        ),
        (
            URB_GT_20K_ADJ,
            'Urban population of 20,000 or more, adjacent to \
                a metro area'
        ),
        (
            URB_GT_20K_NADJ,
            'Urban population of 20,000 or more, not adjacent to \
                a metro area'
        ),
        (
            URB_LT_20K_ADJ,
            'Urban population of 2,500 to 19,999, adjacent to \
                a metro area'
        ),
        (
            URB_LT_20K_NADJ,
            'Urban population of 2,500 to 19,999, not adjacent \
                to a metro area'
        ),
        (
            LT_2K_ADJ,
            'Completely rural or less than 2,500 urban \
                population, adjacent to a metro area'
        ),
        (
            LT_2K_NADJ,
            'Completely rural or less than 2,500 urban \
                population, not adjacent to a metro area'
        )
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
        (
            METRO_GT_1MIL,
            'In large metro area of 1+ million residents'
        ),
        (
            METRO_LT_1MIL,
            'In small metro area of less than 1 million residents'
        ),
        (
            M_ADJ_LM,
            'Micropolitan area adjacent to large metro area'
        ),
        (
            NC_ADJ_LM,
            'Noncore adjacent to large metro area'
        ),
        (
            M_ADJ_SM,
            'Micropolitan area adjacent to small metro area'
        ),
        (
            NC_ADJ_SM_GT_2K,
            'Noncore adjacent to small metro area and contains\
                a town of at least 2,500 residents'
        ),
        (
            NC_ADJ_SM_LT_2K,
            'Noncore adjacent to small metro area and does not\
                contain a town of at least 2,500 residents'
        ),
        (
            M_NADJ_METRO,
            'Micropolitan area not adjacent to a metro area'
        ),
        (
            NC_ADJ_M_GT_2K,
            'Noncore adjacent to micro area and contains a town\
                of at least 2,500 residents'
        ),
        (
            NC_ADJ_M_LT_2K,
            'Noncore adjacent to micro area and does not contain\
                a town of at least 2,500 residents'
        ),
        (
            NC_NADJ_M_GT_2K,
            'Noncore not adjacent to metro or micro area and contains\
                 a town of at least 2,500 residents'
        ),
        (
            NC_NADJ_M_LT_2K,
            'Noncore not adjacent to metro or micro area and does not\
                 contain a town of at least 2,500 residents')
    ]

    urban_continuum_code = models.CharField(
        max_length=1,
        choices=CONTINUUM_CHOICES
    )
    urban_influence_code = models.CharField(
        max_length=2,
        choices=INFLUENCE_CHOICES
    )


class RegionalCases(models.Model):
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    cumulative_cases = models.IntegerField()
    new_cases = models.IntegerField()
    cumulative_deaths = models.IntegerField()
    new_deaths = models.IntegerField()

    unique_together = ['date', 'region']

class RegionalTests(models.Model):
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    cumulative_positive = models.IntegerField(null=True)
    cumulative_negative = models.IntegerField(null=True)
    cumulative_inconclusive = models.IntegerField(null=True)
    new_positive = models.IntegerField(null=True)
    new_negative = models.IntegerField(null=True)
    new_inconclusive = models.IntegerField(null=True)

    unique_together = ['date', 'region']


class DailyTrips(models.Model):
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