class Airport(object):
    def __init__(self):

        fields = [
            'No',
            'Name',
            'ICAO_Code',
            'IATA_Code',
            'Zone',
            'Runway_n',
            'E_n',
            'N_n',
            'Z_ft_n',
            'Z_m_n',
            'Lat_n',
            'Lon_n',
            'Runway_s',
            'E_s',
            'N_s',
            'Z_ft_s',
            'Z_m_s',
            'Lat_s',
            'Lon_s',
            'Z_ft_ARP',
            'Z_m_ARP',
            'RWY_WID',
            'RSW',
            'Code_No',
            'Code_Ltr',
            'Instrument',
            'Precision',
            'ARPE',
            'ARPN',
            'N_TO_InEdge',
            'S_TO_InEdge',

        ]
    def __str__(self):
        return f"Airport({self.name})"
