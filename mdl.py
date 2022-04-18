# -*- coding: cp1252 -*-
import sys
import os
import math
import csv
import EnvSettings

from osgeo import osr
APDATA = open('AirportData.csv','r')
    
def U_W(easting, northing, zone, elev):
    utm_coordinate_system = osr.SpatialReference()
    utm_coordinate_system.SetWellKnownGeogCS("WGS84") # Set geographic coordinate system to handle lat/lon
    is_northern = northing < 0    
    utm_coordinate_system.SetUTM(zone, is_northern)

    wgs84_coordinate_system = utm_coordinate_system.CloneGeogCS() # Clone ONLY the geographic coordinate system 

    # create transform component
    utm_to_wgs84_transform = osr.CoordinateTransformation(utm_coordinate_system,wgs84_coordinate_system) # (<from>, <to>)
    
    lat, lon, alt = utm_to_wgs84_transform.TransformPoint(easting, northing, elev) # returns lon, lat, altitude
    return lat, lon, alt
def W_U(longitude, latitude, elev):    
    def get_utm_zone(longitude):
        return (int(1+(longitude+180.0)/6.0))
        
    def is_northern(latitude):
        """
        Determines if given latitude is a northern for UTM
        """
        if (latitude < 0.0):
            return 0
        else:
            return 1
    guz = get_utm_zone(longitude)
    utm_coordinate_system = osr.SpatialReference()
    utm_coordinate_system.SetWellKnownGeogCS("WGS84") # Set geographic coordinate system to handle lat/lon  
    utm_coordinate_system.SetUTM(get_utm_zone(longitude), is_northern(latitude))

    wgs84_coordinate_system = utm_coordinate_system.CloneGeogCS() # Clone ONLY the geographic coordinate system 

    # create transform component
    wgs84_to_utm_transform = osr.CoordinateTransformation(wgs84_coordinate_system, utm_coordinate_system) # (<from>, <to>)
    return wgs84_to_utm_transform.TransformPoint(longitude, latitude, elev,guz) # returns easting, northing, altitude


#Converts feet to metres and vice versa
def F_M(value, F2M1_or_M2F2):
    if F2M1_or_M2F2 == 1:
        return value*152.4/500
    if F2M1_or_M2F2 == 2:
        return value*500/152.4

#Checking if input is number (float or int)
def IsNum(s):
    try:
        float(s)
        return True
    except ValueError: 
        return False

#Checking if input is Y/y or N/n and returns Y / N
def IsYyNn(s):
    if s == 'Y' or s == 'y':
        return 'Y'
    if s == 'N' or s == 'n':
        return 'N'
    else:
        return False

#checking if input for PIA runways is good and returns Y1 / Y2 / Y3 / N
def IsY1Y2Y3N(s,c):
        if s == 'Y1' or s == 'y1':
            if c == 1 or c == 2 or c == 3 or c == 4:
                return 'Y1'
            else:
                return False
        elif s == 'Y2' or s == 'y2':
            if c == 3 or c == 4:
                return 'Y2'
            else:
                return False
        elif s == 'Y3' or s == 'y3':
            if c == 3 or c == 4:
                return 'Y3'
            else:
                return False
        elif s == 'N' or s == 'n':
            return 'N'
        else:
            return False
        
#Checking if input is F/f or M/m and returns M / F
def IsFfMm(s):
    if s == 'F' or s == 'f':
        return 'F'
    elif s == 'M' or s == 'm':
        return 'M'

    else:
        return False

#Checking if code letter input is correct
def CodeL(s):
    if s.lower() == 'ala':
        return 'ALA'
    if s.lower() == 'a':
        return 'A'
    elif  s.lower()  == 'b':
        return 'B'
    elif s.lower()  == 'c':
        return 'C'
    elif s.lower()  == 'd':
        return 'D'
    elif s.lower()  == 'e':
        return 'E'
    elif s.lower()  == 'f':
        return 'F'
    else:
        return False


def CodeN(s):
    if s.lower() == 'ala':
        return 'ALA'
    elif s == '1' or s == '2' or s == '3' or s == '4':
        try:
            float(s)
            return True
        except ValueError: 
            return False
            return True
    else:
        return False

def isProj(s):
    if s == 'utm' or s == 'UTM':
        return 'UTM'
    elif  s == 'WGS84' or s == 'wgs84':
        return 'WGS84'
    else:
        return False
def isLON_DD(s,ew):
    if s >= -180 and s <= 0 and ew == 'W':
        return s
    elif s <= 180 and s >= 0 and ew == 'E':
        return s
    else:
        return False
def isLAT_DD(s,ns):
    if s >= -90 and s <= 0 and ns == 'S':
        return s
    elif s <= 90 and s >= 0 and ns == 'N':
        return s
    else:
        return False
def isNS_EW(nsew):
    ns = nsew
    ew = nsew  
    if ns == 'n' or ns == 'N' or ns == 'north' or ns == 'North' or ns == 'NORTH':
        return 'N'
    elif ns == 's' or ns == 'S' or ns == 'south' or ns == 'South' or ns == 'SOUTH':
        return 'S'
    elif ew == 'e' or ew == 'E' or ew == 'east' or ew == 'East' or ew == 'EAST':
        return 'E'
    elif ew == 'w' or ew == 'W' or ew == 'west' or ew == 'West' or ew == 'WEST':
        return 'W'
    else:
        return False



def iN(Input_Accuracy):
    A = Input_Accuracy
    while IsNum(A) == False:
        ##print ''
        ##print 'Please ensure you enter numbers only. Try again.'
        A = raw_input("Insert size of surface cells in metres (i.e. enter a, such that cell = a*a): ")
    A = float(A)
    return A

def iS(Input_Accuracy):
    A = Input_Accuracy
    while IsNum(A) == False:
        ##print ''
        ##print 'Please ensure you enter numbers only. Try again.'
        A = raw_input("Insert size of surface cells in metres (i.e. enter a, such that cell = a*a): ")
    A = float(A)
    return A

def AirportData(KML_NAME):
    Dat = []
    for row in csv.reader(APDATA):
        if row[1] ==KML_NAME:
            Dat.append(row)
    return Dat

def SelectedData(KML_NAME,runway):
    D = AirportData(KML_NAME)
    for row in range(len(D)):
        ##print 'flag1','KML_NAME=',KML_NAME,'row[0]=',row[0],'runway=',runway,'row[1]=',row[1]
        if D[row][1] ==KML_NAME and D[row][0] == runway:
            return D[row]
            ##print D[row] 
        else:
            return False
        
def rwyID(KML_NAME):
    rwy = []
    for row in csv.reader(APDATA):
        if row[1] ==KML_NAME:
            rwy.append([row[0],row[5],row[12]])
    return rwy

class Data:
    #Threshold UTM Coordinates
    KML_NAME = input('Type the name of the airport: ')

    rwyDat = []
    ##print 'Choose a corresponding number below: '
    for row in csv.reader(APDATA):
        if KML_NAME == row[1]:
            ##print row[0],row[2],'Runway',row[5],'/',row[12]
            rwyDat.append(row)
    if len(rwyDat) <1:
        print (KML_NAME,"isn't on the AirportData.csv list.",'''

    You may either:
        1) press "Ctrl+C", enter data into AirportData.csv and start again; or
        2) proceed with providing answers as prompted by the following questions.
        ''')
    else:
        ChooseRwy = input('Enter number: ')

    def SelectedData(rwyDat,ChooseRwy,KML_NAME):
        for x in range(len(rwyDat)):
            if ChooseRwy == rwyDat[x][0] and KML_NAME == rwyDat[x][1]:
                return rwyDat[x]

    ap = SelectedData(rwyDat,ChooseRwy,KML_NAME)[1]        
    Zone = SelectedData(rwyDat,ChooseRwy,KML_NAME)[4]
    NTSH = SelectedData(rwyDat,ChooseRwy,KML_NAME)[5]
    NTE = SelectedData(rwyDat,ChooseRwy,KML_NAME)[6]
    NTN = SelectedData(rwyDat,ChooseRwy,KML_NAME)[7]
    STSH = SelectedData(rwyDat,ChooseRwy,KML_NAME)[12]
    STE = SelectedData(rwyDat,ChooseRwy,KML_NAME)[13]
    STN = SelectedData(rwyDat,ChooseRwy,KML_NAME)[14]

    ##print 'You need to tell OLS_Engine where to save your new file named: ',KML_NAME,'.'
    #KML_PATH = raw_input("Copy and paste the directory pathway you want your new KML to be located: ")
    KML_PATH = os.path.join(os.getcwd(),'v0.2')
    if not os.path.exists(KML_PATH):
        os.mkdir(KML_PATH)

    completeName = os.path.join(KML_PATH, KML_NAME+".kml")
    NewKML = KML_NAME
    f = open(completeName, 'w')
    
    ReportData = os.path.join(KML_PATH,"Obstacle Report"+".txt")
    rep=open(ReportData, 'w')

    projType = 'utm'#raw_input("Enter the data projection type (WGS84, UTM): ")
    while isProj(projType) == False:
        ##print ''
        ##print 'Please ensure you enter a valid response. Try again.'
        projType = raw_input("Enter the data projection type (WGS84, UTM): ")
    projType = isProj(projType)

    if projType == 'UTM':
        zone = SelectedData(rwyDat,ChooseRwy,KML_NAME)[4] #raw_input("Enter the UTM zone number: ")
        while IsNum(zone) == False:
            ##print ''
            ##print 'Please ensure you enter numbers only. Try again.'
            zone = raw_input("Enter the UTM zone number: ")
        zone = int(zone)

        #NTE = raw_input("Enter Northern Threshold Eastings UTM Coordinates: ")
        NTE = SelectedData(rwyDat,ChooseRwy,KML_NAME)[6]
        ##print NTE
        while IsNum(NTE) == False:
            ##print ''
            ##print 'Please ensure you enter numbers only. Try again.'
            NTE = raw_input("Enter Northern Threshold Eastings UTM WGS84 Coordinates: ")
        NTE = float(NTE)

        #NTN = raw_input("Enter Northern Threshold Northings UTM_WGS84 Coordinates: ")
        NTN =  SelectedData(rwyDat,ChooseRwy,KML_NAME)[7]

        while IsNum(NTN) == False:
            ##print ''
            ##print 'Please ensure you enter numbers only. Try again.'
            NTN = raw_input("Enter Northern Threshold Northings UTM WGS84 Coordinates: ")
        NTN = float(NTN)


        #STE = raw_input("Enter Southern Threshold Eastings UTM WGS84 Coordinates: ")
        STE =  SelectedData(rwyDat,ChooseRwy,KML_NAME)[13]
        ##print STE
        while IsNum(STE) == False:
            ##print ''
            ##print 'Please ensure you enter numbers only. Try again.'
            STE = raw_input("Enter Southern Threshold Eastings UTM WGS84 Coordinates: ")
        STE = float(STE)

        #STN = raw_input("Enter Southern Threshold Northings UTM WGS84 Coordinates: ")
        STN =   SelectedData(rwyDat,ChooseRwy,KML_NAME)[14]
 
        while IsNum(STN) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            STN = raw_input("Enter Southern Threshold Northings UTM WGS84 Coordinates: ")
        STN = float(STN)
        
        #ARPE = raw_input("Enter ARP Eastings UTM Coordinates: ")
        ARPE = SelectedData(rwyDat,ChooseRwy,KML_NAME)[27]
        #print ARPE
        while IsNum(ARPE) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            ARPE = raw_input("Enter ARP Eastings UTM WGS84 Coordinates: ")
        ARPE = float(ARPE)

        #ARPN = raw_input("Enter ARP Northings UTM Coordinates: ")
        ARPN = SelectedData(rwyDat,ChooseRwy,KML_NAME)[28]
        #print ARPN
        while IsNum(ARPN) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            ARPN = raw_input("Enter ARP Northings UTM WGS84 Coordinates: ")
        ARPN = float(ARPN)
        
    if projType == 'WGS84':
        ns = raw_input("Enter n if north (i.e. +), or s if south (i.e. -), of the equator: ")
        while isNS_EW(ns) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            ns = raw_input("Enter n if north (i.e. +), or s if south (i.e. -), of the equator: ")
        ns = isNS_EW(ns)
        ew = raw_input("Enter e if east (i.e. +) , or w if west (i.e. -), of the the prime meridium: ")
        while isNS_EW(ew) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            ew = raw_input("Enter e if east (i.e. +) , or w if west (i.e. -), of the the prime meridium: ")
        ew = isNS_EW(ew)

        NTlat = raw_input("Enter Northern Threshold latitude in decimal degrees: ")
        while IsNum(NTlat) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            NTlat = raw_input("Enter Northern Threshold latitude in decimal degrees: ")
        NTlat = float(NTlat)
        if ns == 'N':
            NTlat= math.sqrt(math.pow(NTlat,2))
        elif ns == 'S':
            NTlat= math.sqrt(math.pow(NTlat,2))*-1
        while isLAT_DD(NTlat,ns) == False:
            #print ''
            #print 'Please ensure you enter a valid response only. Try again.'
            NTlat = raw_input("Enter Northern Threshold latitude in decimal degrees: ")       
        NTlat=isLAT_DD(NTlat,ns)

        NTlon = raw_input("Enter Northern Threshold longitude in decimal degrees: ")
        while IsNum(NTlon) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            NTlon = raw_input("Enter Northern Threshold longitude in decimal degrees: ")
        NTlon = float(NTlon)
        if ew == 'E':
            NTlon= math.sqrt(math.pow(NTlon,2))
        elif ew == 'W':
            NTlon= math.sqrt(math.pow(NTlon,2))*-1
        while isLON_DD(NTlon,ew) == False:
            #print ''
            #print 'Please ensure you enter a valid response only. Try again.'
            NTlon = raw_input("Enter Northern Threshold latitude in decimal degrees: ")       
        NTlon=isLON_DD(NTlon,ew)



        STlat = raw_input("Enter Southern Threshold latitude in decimal degrees: ")
        while IsNum(STlat) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            STlat = raw_input("Enter Northern Threshold latitude in decimal degrees: ")
        STlat = float(STlat)
        if ns == 'N':
            STlat= math.sqrt(math.pow(STlat,2))
        elif ns == 'S':
            STlat= math.sqrt(math.pow(STlat,2))*-1
        while isLAT_DD(STlat,ns) == False:
            #print ''
            #print 'Please ensure you enter a valid response only. Try again.'
            STlat = raw_input("Enter Northern Threshold latitude in decimal degrees: ")       
        STlat=isLAT_DD(STlat,ns)

        STlon = raw_input("Enter Northern Threshold longitude in decimal degrees: ")
        while IsNum(STlon) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            STlon = raw_input("Enter Northern Threshold longitude in decimal degrees: ")
        STlon = float(STlon)
        if ew == 'E':
            STlon= math.sqrt(math.pow(STlon,2))
        elif ew == 'W':
            STlon= math.sqrt(math.pow(STlon,2))*-1
        while isLON_DD(STlon,ew) == False:
            #print ''
            #print 'Please ensure you enter a valid response only. Try again.'
            NTlon = raw_input("Enter Northern Threshold latitude in decimal degrees: ")       
        STlon=isLON_DD(STlon,ew)

    #Feet or Metres?

    #ForM = raw_input("Are the Threshold Elevation values in Metres or Feet (m / f)? ")
    ForM = 'm'
    ForM = IsFfMm(ForM)
    while IsFfMm(ForM) == False:
        #print ''
        #print 'Please ensure you enter either m or f only. Try again.'
        ForM = raw_input("Are the Threshold Elevation values in Metres or Feet (m / f)? ")
    ForM = IsFfMm(ForM)

    if ForM == 'F' or ForM == 'f':
        ForM = 'F'
        #NEF = raw_input("Enter Northern Threshold Elevation in Feet: ")
        NEF = SelectedData(rwyDat,ChooseRwy,KML_NAME)[8]
        while IsNum(NEF) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            NEF = raw_input("Enter Northern Threshold Elevation in Feet: ")
        NE = F_M(float(NEF),1)

        #SEF = raw_input("Enter Southern Threshold Elevation in Feet: ")
        SEF = SelectedData(rwyDat,ChooseRwy,KML_NAME)[15]
        while IsNum(SEF) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            SEF = raw_input("Enter Southern Threshold Elevation in Feet: ")
        SE = F_M(float(SEF),1)

        #ARPf = raw_input("Enter Aerodrome Reference Point (ARP) Elevation in Feet: ")
        ARPf = SelectedData(rwyDat,ChooseRwy,KML_NAME)[19]
        while IsNum(ARPf) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            ARPf = raw_input("Enter Aerodrome Reference Point (ARP) Elevation in Feet: ")
        ARP = F_M(float(ARPf),1)
        ARPf = float(ARPf)
        
    if ForM == 'M' or ForM == 'm':
        ForM = 'M'
        #NEM = raw_input("Enter Northern Threshold Elevation in Metres: ")
        NEM = SelectedData(rwyDat,ChooseRwy,KML_NAME)[9]
        while IsNum(NEM) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            NEM = raw_input("Enter Northern Threshold Elevation in Metres: ")
        NE = float(NEM)
        
        #SEM = raw_input("Enter Southern Threshold Elevation in Metres: ")
        SEM = SelectedData(rwyDat,ChooseRwy,KML_NAME)[16]
        while IsNum(SEM) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            SEM = raw_input("Enter Southern Threshold Elevation in Metres: ")
        SE = float(SEM)
        #ARPm = raw_input("Enter Aerodrome Reference Point (ARP) elevation in Metres: ")
        ARPm = SelectedData(rwyDat,ChooseRwy,KML_NAME)[20]
        
        while IsNum(ARPm) == False:
            #print ''
            #print 'Please ensure you enter numbers only. Try again.'
            ARPm = raw_input("Enter Aerodrome Reference Point (ARP) elevation in Metres: ")
        ARP = float(ARPm)
        ARPm = float(ARPm)
    if projType == 'WGS84':
        Nth = list(W_U(NTlon, NTlat, NE))
        z1 = Nth[3]
        Sth = list(W_U(STlon, STlat, SE))
        z2 = Sth[3]
        NTE = Nth[0]
        NTN = Nth[1]
        STE = Sth[0]
        STN = Sth[1]
        if z1 == z2:
            zone = int(z1)
        else:
            print ('Something went wrong with the zone calculations')

    #CN = raw_input("Enter Runway Code Number: ")
    CN = SelectedData(rwyDat,ChooseRwy,KML_NAME)[23]
    while CodeN(CN) == False:
        #print ''
        #print 'Please ensure you enter numbers only from 1 to 4 or "ALA". Try again.'
        CN = raw_input("Enter Runway Code Number: ")
    if CN == 'ALA':
        CN = 'ALA'
    else:
        CN = float(CN)


    #CL  = raw_input("Enter Runway Code Letter: ")
    CL  = SelectedData(rwyDat,ChooseRwy,KML_NAME)[24]
    while CodeL(CL) == False:   
        #print ''
        #print 'Please ensure you enter either A to F only. Try again.'
        CL = raw_input("Enter Runway Code Letter: ")
    if CL == 'ALA':
        CL = None
    else:
        CL = CodeL(CL)

    #NIns = raw_input("Is the Southern Approach runway an instrument runway (Y / N)? ")
    NIns = SelectedData(rwyDat,ChooseRwy,KML_NAME)[25]
    while IsYyNn(NIns) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        NIns = raw_input("Is the Southern Approach runway an instrument runway (Y / N)? ")
    NIns = IsYyNn(NIns)
    #STOIns = raw_input("Is the Southern Take-off runway an instrument runway (Y / N)? ")
    STOIns = 'N'
    while IsYyNn(STOIns) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        STOIns = raw_input("Is the Southern take-off runway an instrument runway (Y / N)? ")
    STOIns = IsYyNn(STOIns)

    #SIns = raw_input("Is the Northern Approach runway an instrument runway (Y / N)? ")
    SIns = SelectedData(rwyDat,ChooseRwy,KML_NAME)[25]
    while IsYyNn(SIns) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        SIns = raw_input("Is the Northern Approach runway an instrument runway (Y / N)? ")
    SIns = IsYyNn(SIns)
    #NTOIns = raw_input("Is the Northern Take-off runway an instrument runway (Y / N)? ")
    NTOIns = 'N'
    while IsYyNn(NTOIns) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        NTOIns = raw_input("Is the Northern take-off runway an instrument runway (Y / N)? ")
    NTOIns = IsYyNn(NTOIns)

    if NIns == 'Y':
        #NPrc = raw_input("Is the Southern Approach runway a precision instrument runway (Y1 / Y2 / Y3 / N)? ")
        NPrc = SelectedData(rwyDat,ChooseRwy,KML_NAME)[26]
        while IsY1Y2Y3N(NPrc,CN) == False:   
            #print ''
            #print 'Please ensure you enter either Y or N only. Try again.'
            #print 'Please also ensure the Code No. and Precision Approach CAT No. combination is valid.'
            #print 'If you need to use another code number, press Ctrl+C to start again.'
            NPrc = raw_input("Is the Southern Approach runway a precision instrument runway (Y1 / Y2 / Y3 / N)? ")
        NPrc = IsY1Y2Y3N(NPrc,CN)
        if NPrc == 'Y1' or NPrc == 'Y2' or NPrc == 'Y3':
            if CN == 1 or CN == 2 or CN == 3 or CN == 4:
                #NBLDist = raw_input("For the Northern Approach Baulked Landing surface, enter the distance of the surface from the threshold: ")
                NBLDist = '1800'
                while IsNum(NBLDist) == False:
                    #print ''
                    #print 'Please ensure you enter numbers only. Try again.'

                    NBLDist = raw_input("For the Northern Approach Baulked Landing surface, enter the distance of the surface from the threshold: ")
                NBLDist = float(NBLDist)
        if NPrc == 'N':
            NRunwayInfo = ' Instrument non-precision'
        elif NPrc == 'Y1':
             NRunwayInfo = ' Instrument precision (cat1)'
        elif NPrc == 'Y2':
            NRunwayInfo = ' Instrument precision (cat2)'
        elif NPrc == 'Y3':
           NRunwayInfo = ' Instrument precision (cat3)'
    elif NIns == 'N':
        NRunwayInfo = ' Non-instrument'
        

    if SIns == 'Y':
        #SPrc = raw_input("Is the Northern Approach runway a precision instrument runway (Y1 / Y2 / Y3 / N)? ")
        SPrc = SelectedData(rwyDat,ChooseRwy,KML_NAME)[26]
        while IsY1Y2Y3N(SPrc,CN) == False:   
            #print ''
            #print 'Please ensure you enter either Y or N only. Try again.'
            #print 'Please also ensure the Code No. and Precision Approach CAT No. combination is valid.'
            #print 'If you need to use another code number, press Ctrl+C to start again.'
            SPrc = raw_input("Is the Northern Approach runway a precision instrument runway (Y1 / Y2 / Y3 / N)? ")
        SPrc = IsY1Y2Y3N(SPrc,CN)
        if SPrc == 'Y1' or SPrc == 'Y2' or SPrc == 'Y3':
            if CN == 1 or CN == 2 or CN == 3 or CN == 4:
                #SBLDist = raw_input("For the Northern Approach Baulked Landing surface, enter the distance of the surface from the threshold: ")
                SBLDist = '1800'
                while IsNum(SBLDist) == False:
                    #print ''
                    #print 'Please ensure you enter numbers only. Try again.'
                    
                    SBLDist = raw_input("For the Northern Approach Baulked Landing surface, enter the distance of the surface from the threshold: ")
                SBLDist = float(SBLDist)
        if SPrc == 'N':
            SRunwayInfo = ' Instrument non-precision'
        elif SPrc == 'Y1':
             SRunwayInfo = ' Instrument precision (cat1)'
        elif SPrc == 'Y2':
            SRunwayInfo = ' Instrument precision (cat2)'
        elif SPrc == 'Y3':
           SRunwayInfo = ' Instrument precision (cat3)'
    elif SIns == 'N':
        SRunwayInfo = ' Non-instrument'

    #RWY_WID = raw_input("Enter Runway Width in metres: ")
    RWY_WID = SelectedData(rwyDat,ChooseRwy,KML_NAME)[21]
    while IsNum(RWY_WID) == False:
        #print ''
        #print 'Please ensure you enter numbers only. Try again.'
        RWY_WID = raw_input("Enter Runway Width in metres: ")
    RWY_WID = float(RWY_WID)

    NCLWY =   SelectedData(rwyDat,ChooseRwy,KML_NAME)[29]
    while IsNum(NCLWY) == False:
        #print ''
        #print 'Please ensure you enter numbers only. Try again.'
        NCLWY = raw_input("Enter Take-off Innder Edge distance: ")
    NCLWY = float(NCLWY)

    SCLWY =   SelectedData(rwyDat,ChooseRwy,KML_NAME)[30]
    while IsNum(SCLWY) == False:
        #print ''
        #print 'Please ensure you enter numbers only. Try again.'
        SCLWY = raw_input("Enter Take-off Innder Edge distance: ")
    SCLWY = float(SCLWY)


##    #NCLWY = raw_input("Enter the length of the northern clearway in metres: ")
##    NCLWY = 60
##    while IsNum(NCLWY) == False:
##        #print ''
##        #print 'Please ensure you enter numbers only. Try again.'
##        NCLWY = raw_input("Enter the length of the northern clearway in metres: ")
##    NCLWY = float(NCLWY)
##    #SCLWY = raw_input("Enter the length of the southern clearway in metres: ")
##    SCLWY = 60
##    while IsNum(SCLWY) == False:
##        #print ''
##        #print 'Please ensure you enter numbers only. Try again.'
##        SCLWY = raw_input("Enter the length of the southern clearway in metres: ")
##    SCLWY = float(SCLWY)
    #RSW = raw_input("Enter Runway Strip Width in metres: ")
    
    RSW = SelectedData(rwyDat,ChooseRwy,KML_NAME)[22]
    while IsNum(RSW) == False:
        #print ''
        #print 'Please ensure you enter numbers only. Try again.'
        RSW = raw_input("Enter Runway Strip Width in metres: ")
    RSW = float(RSW)

    #DayOnly  = raw_input("Is the runway used in day only (Y / N): ")
    DayOnly  = 'N'
    while IsYyNn(DayOnly) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        DayOnly = raw_input("Is the runway used in day only (Y / N): ")
    DayOnly = IsYyNn(DayOnly)

    #NMTOW22700kg = raw_input("Do aircraft with MTOW >= 22700 kg operate on the northern take-off runway? (Y / N): ")
    NMTOW22700kg = 'Y'
    while IsYyNn(NMTOW22700kg) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        NMTOW22700kg = raw_input("Do aircraft with MTOW >= 22700 kg operate on the northern take-off runway? (Y / N): ")
    NMTOW22700kg = IsYyNn(NMTOW22700kg)

    if NMTOW22700kg == 'Y':
        NMTOW5700kg = 'Y'
    elif NMTOW22700kg == 'N':
        #NMTOW5700kg = raw_input("Do aircraft with MTOW >= 5700 kg operate on the northern take-off runway? (Y / N): ")
        NMTOW5700kg = 'Y'
        while IsYyNn(NMTOW5700kg) == False:   
            #print ''
            #print 'Please ensure you enter either Y or N only. Try again.'
            NMTOW5700kg = raw_input("Do aircraft with MTOW >= 5700 kg operate on the northern take-off runway? (Y / N): ")
        NMTOW5700kg = IsYyNn(NMTOW5700kg)
        
    #NMTOW22700kg = raw_input("Do aircraft with MTOW >= 22700 kg operate on the southern take-off runway? (Y / N): ")
    SMTOW22700kg = 'y'
    while IsYyNn(SMTOW22700kg) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        SMTOW22700kg = raw_input("Do aircraft with MTOW >= 22700 kg operate on the southern take-off runway? (Y / N): ")
    SMTOW22700kg = IsYyNn(SMTOW22700kg)

    if SMTOW22700kg == 'Y':
        SMTOW5700kg = 'Y'
    elif SMTOW22700kg == 'N':
        #SMTOW5700kg = raw_input("Do aircraft with MTOW >= 5700 kg operate on the southern take-off runway? (Y / N): ")
        SMTOW5700kg = 'Y'
        while IsYyNn(SMTOW5700kg) == False:   
            #print ''
            #print 'Please ensure you enter either Y or N only. Try again.'
            SMTOW5700kg = raw_input("Do aircraft with MTOW >= 5700 kg operate on the southern take-off runway? (Y / N): ")
        SMTOW5700kg = IsYyNn(SMTOW5700kg)
    MTOW5700kg = IsYyNn('Y')

    #TOLength = raw_input("What is the length of the northern take-off area (m): ")
    NTOL = '10000'
    while IsNum(NTOL) == False:
        #print ''
        #print 'Please ensure you enter numbers only. Try again.'
        NTOL = raw_input("What is the length of the northern take-off area (m): ")
    NTOL = float(NTOL)
    #TOLength = raw_input("What is the length of the southern take-off area (m): ")
    STOL = '10000'
    while IsNum(STOL) == False:
        #print ''
        #print 'Please ensure you enter numbers only. Try again.'
        STOL = raw_input("What is the length of the southern take-off area (m): ")
    STOL = float(STOL)

    #NTOAlt = raw_input("Is an alternative northern take-off area required?(Y / N): ")
    NTOAlt = 'N'
    while IsYyNn(NTOAlt) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        NTOAlt = raw_input("Is an alternative northern take-off area required? (Y / N)")
    NTOAlt = IsYyNn(NTOAlt)
    #STOAlt = raw_input("Is an alternative southern take-off area required?(Y / N): ")
    STOAlt = 'N'
    while IsYyNn(STOAlt) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        STOAlt = raw_input("Is an alternative southern take-off area required? (Y / N)")
    STOAlt = IsYyNn(STOAlt)

    #JetTransport = raw_input("Are there Jet Transport Aeroplanes operating on the runway?(Y / N): ")
    JetTransport = 'Y'
    while IsYyNn(JetTransport) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        JetTransport = raw_input("Are there Jet Transport Aeroplanes operating on the runway?(Y / N): ")
    JetTransport = IsYyNn(JetTransport)

    #RwyWid30 = raw_input("Do aircraft operating on the runway only require a runway <= 30 wide?(Y / N): ")
    RwyWid30 = 'N'
    while IsYyNn(RwyWid30) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        RwyWid30 = raw_input("Do aircraft operating on the runway only require a runway <= 30 wide?(Y / N): ")
    RwyWid30 = IsYyNn(RwyWid30)

    #RPT = raw_input("Is the runway used by RPT aircraft? (Y / N): ")
    RPT = 'Y'
    while IsYyNn(RPT) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        RPT = raw_input("Is the runway used by RPT aircraft? (Y / N): ")
    RPT =   IsYyNn(RPT)

    #VMC = raw_input("Is the runway used only in VMC? (Y / N): ")
    VMC = 'N'
    while IsYyNn(VMC) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        VMC = raw_input("Is the runway used only in VMC? (Y / N): ")
    VMC = IsYyNn(VMC)

    #NTOTurn15d = raw_input("Is there a northern take-off procedure that has a turn >15 degrees? (Y / N): ")
    NTOTurn15d = 'N'
    while IsYyNn(NTOTurn15d) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        NTOTurn15d = raw_input("Is there a northern take-off procedure that has a turn >15 degrees? (Y / N): ")
    NTOTurn15d =   IsYyNn(NTOTurn15d)
    #STOTurn15d = raw_input("Is there a southern take-off procedure that has a turn >15 degrees? (Y / N): ")
    STOTurn15d = 'N'
    while IsYyNn(STOTurn15d) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        STOTurn15d = raw_input("Is there a southern take-off procedure that has a turn >15 degrees? (Y / N): ")
    STOTurn15d =   IsYyNn(STOTurn15d)

    ##TPSlope = raw_input("Can the take-off slope be reduced from 2% to 1.6%? (Y / N): ")
    TPSlope = 'N'
    while IsYyNn(TPSlope) == False:   
        #print ''
        #print 'Please ensure you enter either Y or N only. Try again.'
        TOTurn15d = raw_input("Can the take-off slope be reduced from 2% to 1.6%? (Y / N): ")
    TPSlope =   IsYyNn(TPSlope)

##    if math.fabs(ARP) - (SE+NE)/2 >= 3:
##        RED = (SE+NE)/2
##    elif math.fabs(ARP) - (SE+NE)/2 < 3:
##        RED = ARP
##    RED = math.floor(2*RED)/2
    RED = 22.5


        
#Data Generator
def toUTM(NTE,NTN,STE,STN,ARP,SE,NE,par,perp,zDif,n_s):
    if n_s == 'n':
        deg = 180+(math.degrees(math.atan((NTE-STE)/(NTN-STN))))
    elif n_s == 's':
        deg = (math.degrees(math.atan((NTE-STE)/(NTN-STN))))

    if perp>=0:
        eDif = par*math.sin(math.radians(deg))+math.fabs(perp)*math.sin(math.radians(deg + 90))
        nDif = par*math.cos(math.radians(deg))+math.fabs(perp)*math.cos(math.radians(deg + 90))
        
    elif perp < 0:
        eDif = par*math.sin(math.radians(deg))+math.fabs(perp)*math.sin(math.radians(deg - 90))
        nDif = par*math.cos(math.radians(deg))+math.fabs(perp)*math.cos(math.radians(deg - 90))    
    if math.fabs(ARP) - (SE+NE)/2 >= 3:
        RED = (SE+NE)/2
    elif math.fabs(ARP) - (SE+NE)/2 < 3:
        RED = ARP
    RED = math.floor(2*RED)/2
    zVal = RED + zDif
    if n_s == 'n':
        Easts = NTE + eDif
        Norths = NTN + nDif
    elif n_s == 's':
        Easts = STE + eDif
        Norths = STN + nDif
    pwn = [Easts,Norths,zVal]
    return pwn
