from django.db import models


class Aerodrome(models.Model):
    name = models.CharField(max_length=200)
    icao_code = models.CharField(max_length=4)
    
    utm_zone = models.IntegerField( )
    arp_northings = models.FloatField('Aerodrome Reference Point Northings')
    arp_eastings = models.FloatField('Aerodrome Reference Point Eastings')
    arp_height = models.FloatField('Aerodrome Reference Point Height')

    def __str__(self):
        return f"{self.name}"

class Runway(models.Model):
    aerodrome = models.ForeignKey(Aerodrome, on_delete=models.CASCADE)
    name = models.CharField(max_length=3)
    runway_code_number = models.CharField(max_length=3)
    runway_code_letter = models.CharField(max_length=3)

    INSTRUMENT_CHOICES = [
        ('N', 'Non instrument'),
        ('Y', 'Instrument'),
        ]
    instrument = models.CharField(max_length=1, choices=INSTRUMENT_CHOICES)

    PRECISION_CHOICES = [('N', 'Non precision'),
                         ('1', 'Precision cat 1'),
                         ('2', 'Precision cat 2'),
                         ('3a', 'Precision cat 3a'),
                         ('3b', 'Precision cat 3b'),
                         ('3c', 'Precision cat 3c'),
                         ]
    precision = models.CharField(max_length=2, choices=PRECISION_CHOICES)
    
    approach_end_eastings = models.FloatField()
    approach_end_northings = models.FloatField()
    approach_end_height = models.FloatField()
    
    takeoff_end_eastings = models.FloatField()
    takeoff_end_northings = models.FloatField()
    takeoff_end_height = models.FloatField()

    runway_width = models.FloatField()
    runway_strip_width = models.FloatField()

    takeoff_inner_edge = models.FloatField()
    
    
    def __str__(self):
        return f"{self.name}"    
