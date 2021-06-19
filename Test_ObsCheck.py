import sys
import os
import math
import OLSDims
import EnvSettings

##try:
from osgeo import osr
##    from osgeo import gdal
##except ImportError:
#import osr
##    import gdal

print """


--------------------------------------------------
Welcome to the beta version of the OLS Engine v0.2.
--------------------------------------------------
Release date: 4 April 2016.

OLS Engine allows you to generate your own
Obstacle Limitation Surface (OLS) for your own viewing
in Google Earth.

Google Earth or Google Earth Pro must be installed.

OLS Engine relies on data input from you in order to
generage the OLS. This input data is standard for any OLS.

In order to generate your OLS, simply answer the questions
that OLS Engine asks and follow the guidance provided
within the questions. Google Earth is a great source of
data to answer some of these questions.

OLS Engine will finally ask you how high you wish to
set the resolution of your OLS model in square metres.
E.g. entering 100 means OLS Engine will generate your
OLS with 100 metre square cells. The smaller the number,
the greater the height accuracy but larger the KML file,
and vice versa.

IF YOU RUN INTO ANY ISSUES because of BAD input data,
close the program and restart OLS Engine. This step
should get you back on track.

Once OLS Engine opens your OLS model in Google Earth, you may
customise the style settings, e.g. surface colour, transparency etc.

Please report bugs to Luke Hodgson
lhodgson@aviationprojects.com.au
0411517382

Thank you and I hope you enjoy OLS Engine.

Regards
Luke Hodgson

--------------------------------------------------
Please enter the data input below:
--------------------------------------------------
"""
import mdl
import App
import InApp
import Trans
import InTrans
import Baulked
import IHS
import TO
import Circ
import CAAP92App
import CAAP92Trans
import Conl
import OHS
import ObsData
import Obs_OLS_Check


class dataInput:
    ip = mdl.Data()
    rep=ip.rep
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
        if NPrc != 'N':
            NBLDist=ip.NBLDist
    CN = ip.CN
    DayOnly = ip.CN
    CL=ip.CL
    RED=ip.RED
    MTOW5700kg = ip.MTOW5700kg
    NMTOW22700kg=ip.NMTOW22700kg
    SMTOW22700kg=ip.SMTOW22700kg
    NTOTurn15d=ip.NTOTurn15d
    STOTurn15d=ip.STOTurn15d
    RPT = ip.RPT

    
    SIns = ip.SIns
    if SIns == 'Y':
        SPrc=ip.SPrc
        if SPrc != 'N':
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
    ARPE=ip.ARPE
    ARPN=ip.ARPN
    ARPCoords=[ARPE,ARPN,ARP]
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
    report = Obs_OLS_Check.NorthObsCheck(NToOls,NApOls)	
    print report 
    X = range(len(report))
    print report[0]
    for x in X:
        print str(report[x])
        ip.rep.write(str(report[x]))
        ip.rep.write('\n')
    report = Obs_OLS_Check.SouthObsCheck(SToOls,SApOls)
    print report 
    X = range(len(report))
    print report[0]
    for x in X:
        print str(report[x])
        ip.rep.write(str(report[x]))
        ip.rep.write('\n')