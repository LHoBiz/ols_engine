from django.db import models
from . import src
import os


class Aerodrome(models.Model):
    
    # owner of the Aerodrome object
    owner = models.CharField(max_length=200)
    

    name = models.CharField(max_length=200)
    icao_code = models.CharField(max_length=4)
    iata_code = models.CharField(max_length=4, null=True)

    
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
    approach_inner_edge = models.FloatField()
    
    
    def __str__(self):
        return f"{self.name}"    

    def generate_ols(self):
        fields = "No,Name,ICAO_Code,IATA_Code,Zone,Runway_n,E_n,N_n,Z_ft_n,Z_m_n,Lat_n,Lon_n, Runway_s,E_s,N_s,Z_ft_s,Z_m_s,Lat_s,Lon_s,Z_ft_ARP,Z_m_ARP,RWY_WID,RSW,Code_No,Code_Ltr,Instrument,Precision,ARPE,ARPN,N_TO_InEdge,S_TO_InEdge,,".split(",")
        values = [
            1, 
            self.aerodrome.name,
            self.aerodrome.icao_code,
            self.aerodrome.iata_code,
            self.aerodrome.utm_zone,
            self.name,
            self.approach_end_eastings,
            self.approach_end_northings,
            self.approach_end_height,
            self.approach_end_height,
            None,
            None,
            self.name,
            self.takeoff_end_eastings,
            self.takeoff_end_northings,
            self.takeoff_end_height,
            self.takeoff_end_height,
            None,
            None,
            self.aerodrome.arp_height,
            self.aerodrome.arp_height,
            self.runway_width,
            self.runway_strip_width,
            self.runway_code_number,
            self.runway_code_letter,
            self.instrument,
            self.precision,
            self.aerodrome.arp_eastings,
            self.aerodrome.arp_northings,
            self.approach_inner_edge,
            self.takeoff_inner_edge,
            ]
        for i, value in enumerate(values):
            values[i] = str(value)

        with open(os.path.join(os.path.dirname(__file__), 'src', 'AirportData.csv'), 'w') as airport_data_file:
            airport_data_file.writelines(','.join(fields)+'\n')
            airport_data_file.writelines(','.join(values))
        from .src import OLS_Engine
        OLS_Engine.dataInput(self.aerodrome.name)