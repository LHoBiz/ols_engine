# -*- coding: cp1252 -*-
import WelcomeNote
import math
import OLSDims
import mdl
import EnvSettings
from osgeo import osr
import Circ
import os
import ObsData
class dataInput:
    ip = mdl.Data()
    f=ip.f
    AppOLS = OLSDims.AppDim.AppOLS
    ToOLS = OLSDims.TODim.ToOLS
    AppOLSNAME=OLSDims.AppDim.AppOLSNAME
    AppOLSDIMS=OLSDims.AppDim.AppOLSDIMS
    TOOLSNAME=OLSDims.TODim.TOOLSNAME
    NRunwayInfo=ip.NRunwayInfo
    SRunwayInfo=ip.SRunwayInfo
    NIns = ip.NIns
    if NIns == 'Y':
        NPrc=ip.NPrc
        if NPrc <> 'N':
            NBLDist=ip.NBLDist
    CN = ip.CN
    DayOnly = ip.CN
    CL=ip.CL
    RED=ip.RED
    MTOW5700kg = ip.MTOW5700kg
    RPT = ip.RPT

    
    SIns = ip.SIns
    if SIns == 'Y':
        SPrc=ip.SPrc
        if SPrc <> 'N':
            SBLDist=ip.SBLDist
    RPT = ip.RPT

    
    RWY_WID=ip.RWY_WID
    RSW=ip.RSW
    CodeNo = range(len(AppOLS))
    Surfaces = range(len(AppOLS[0]))
    ToSurfs = range(len(ToOLS[0]))
    NE=ip.NE
    SE=ip.SE
    NTE=ip.NTE
    NTN=ip.NTN
    STE=ip.STE
    STN=ip.STN
    ARP=ip.ARP
    SE=ip.SE
    NE=ip.NE
    zone=ip.zone
    KML_NAME=ip.KML_NAME
    completeName=ip.completeName
    NCLWY=ip.NCLWY
    SCLWY=ip.SCLWY
    NTOIns=ip.NTOIns
    STOIns=ip.STOIns


    RwyLen = math.sqrt((NTE-STE)*(NTE-STE) + (NTN-STN)*(NTN-STN))
    if CN == 'ALA':
        NApOls = []
        SApOls = []
    else:
            
        if NTOIns == 'N':
            if CN == 2:
                NToOls = []
                for i in ToSurfs:
                    NToOls.append(ToOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            NToOls = []
                            for i in ToSurfs:
                                NToOls.append(ToOLS[1][i])                            
                else:
                    NToOls = []
                    for i in ToSurfs:
                        NToOls.append(ToOLS[0][i])
            if CN == 3 or CN == 4:
                NToOls = []
                for i in ToSurfs:
                    NToOls.append(ToOLS[2][i])
                if NMTOW22700kg == 'N' and DayOnly == 'Y':
                    NToOls[0] = 90
                if NTOTurn15d == 'N' and DayOnly == 'Y':
                    NToOls[3] = 1200
        if NTOIns == 'Y':
            if CN == 2:
                NToOls = []
                for i in ToSurfs:
                    NToOls.append(ToOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            NToOls = []
                            for i in ToSurfs:
                                NToOls.append(ToOLS[1][i])                            
                else:
                    NToOls = []
                    for i in ToSurfs:
                        NToOls.append(ToOLS[0][i])
            if CN == 3 or CN == 4:
                NToOls = []
                for i in ToSurfs:
                    NToOls.append(ToOLS[2][i])                
        if NIns == 'N':
            if CN == 2:
                
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            NApOls = []
                            for i in Surfaces:
                                NApOls.append(AppOLS[1][i])                      
                else:
                    NApOls = []
                    NToOls = []
                    for i in Surfaces:
                        NApOls.append(AppOLS[0][i])
                    for i in ToSurfs:
                        NToOls.append(ToOLS[0][i])
            if CN == 3:
                NApOls = []
                NToOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[2][i])
                for i in ToSurfs:
                    NToOls.append(ToOLS[2][i])
                if RWY_WID <= 30:
                    NApOls[3][0] = 90
                if NMTOW22700kg == 'N' and DayOnly == 'Y':
                    NToOls[0] = 90
                if NTOTurn15d == 'N' and DayOnly == 'Y':
                    NToOls[3] = 1200
            if CN == 4:
                NApOls = []
                NToOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[3][i])
                for i in ToSurfs:
                    NToOls.append(ToOLS[2][i])
                if NMTOW22700kg == 'N' and DayOnly == 'Y':
                    NToOls[0] = 90
                if NTOTurn15d == 'N' and DayOnly == 'Y':
                    NToOls[3] = 1200
        if NIns == 'Y' and NPrc == 'N':
            if CN == 1 or CN == 2:
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[4][i])            
            if CN == 3:
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[5][i])
            if CN == 4:
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[6][i])       
        if NIns == 'Y' and NPrc == 'Y1':
            if CN == 1 or CN == 2:
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[7][i])
                NApOls[7][1] = NBLDist
            elif CN == 3 or CN == 4:
                NApOls = []
                
                for i in Surfaces:
                    NApOls.append(AppOLS[8][i])
                if NBLDist <= NApOls[7][1]:
                    NApOls[7][1] = NBLDist
                
        if NIns == 'Y':
            if NPrc == 'Y2' or NPrc == 'Y3':
                if CN == 3 or CN == 4:
                    NApOls = []
                    for i in Surfaces:
                        NApOls.append(AppOLS[9][i])         




        if STOIns == 'N':
            if CN == 2:
                SToOls = []
                for i in ToSurfs:
                    SToOls.append(ToOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            SToOls = []
                            for i in ToSurfs:
                                SToOls.append(ToOLS[1][i])                            
                else:
                    SToOls = []
                    for i in ToSurfs:
                        SToOls.append(ToOLS[0][i])
            if CN == 3 or CN == 4:
                SToOls = []
                for i in ToSurfs:
                    SToOls.append(ToOLS[2][i])
                if SMTOW22700kg == 'N' and DayOnly == 'Y':
                    SToOls[0] = 90
                if STOTurn15d == 'N' and DayOnly == 'Y':
                    SToOls[3] = 1200
        if STOIns == 'Y':
            if CN == 2:
                SToOls = []
                for i in ToSurfs:
                    SToOls.append(ToOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            SToOls = []
                            for i in ToSurfs:
                                SToOls.append(ToOLS[1][i])                            
                else:
                    SToOls = []
                    for i in ToSurfs:
                        SToOls.append(ToOLS[0][i])
            if CN == 3 or CN == 4:
                SToOls = []
                for i in ToSurfs:
                    SToOls.append(ToOLS[2][i])                



        if SIns == 'N':
            if CN == 2:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[1][i]) 
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            SApOls = []
                            for i in Surfaces:
                                SApOls.append(AppOLS[1][i])
                else:
                    SApOls = []
                    for i in Surfaces:
                        SApOls.append(AppOLS[0][i])                         
            if CN == 3:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[2][i])
                if RWY_WID <= 30:
                    SApOls[3][0] = 90
            if CN == 4:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[3][i])
        if SIns == 'Y' and SPrc == 'N':
            if CN == 1 or CN == 2:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[4][i])            
            if CN == 3:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[5][i])
            if CN == 4:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[6][i])
                    
        if SIns == 'Y' and SPrc == 'Y1':
            if CN == 1 or CN == 2:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[7][i])
                SApOls[7][1] = SBLDist            
            if CN == 3 or CN == 4:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[8][i])
                if SBLDist <= SApOls[7][1]:
                    SApOls[7][1] = SBLDist
        if SIns == 'Y':
            if SPrc == 'Y2' or SPrc == 'Y3':
                if CN == 3 or CN == 4:
                    SApOls = []
                    for i in Surfaces:
                        SApOls.append(AppOLS[9][i])

    accur    = raw_input("Insert size of surface cells in metres (i.e. enter a, such that cell = a*a): ")
    colour = "19ff0011"
    string = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>Points</name>
	<Style id="s_ylw-pushpin_hl">
		<IconStyle>
			<color>ff1e8ff7</color>
			<scale>1.2</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>
	<StyleMap id="m_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_ylw-pushpin_hl</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="s_ylw-pushpin">
		<IconStyle>
			<color>ff1e8ff7</color>
			<scale>1.2</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>
	"""
    f.write(string)
    #ObsData.NthObs(NCLWY)
    #ObsData.SthObs(SCLWY)
##    ObsData.NthObs2(NCLWY,NToOls)
##    ObsData.SthObs2(SCLWY,SToOls)
##    ObsData.RwyEnds()
    ObsData.DEM()
    f.write( '</Document>\n')
    f.write( '</kml>\n')

    #f.close()
    os.startfile(completeName)
    print 'OK, done now'


