# -*- coding: cp1252 -*-
import sys
import os
import math
from . import OLSDims
from . import EnvSettings

from osgeo import osr
from . import mdl
ip = mdl.Data()
f=ip.f
AppOLS = OLSDims.AppDim.AppOLS
AppOLSNAME=OLSDims.AppDim.AppOLSNAME
AppOLSDIMS=OLSDims.AppDim.AppOLSDIMS
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

RwyLen = math.sqrt((NTE-STE)*(NTE-STE) + (NTN-STN)*(NTN-STN))

def NInApp(ApOls,accur):
    E1 = NE
    E2 = SE
    ns = 'n'
    Surf = 'NorthInnerAppoach'
    InnerApp(E1,E2,ns,Surf,accur,ApOls)
def SInApp(ApOls,accur):
    E1 = SE
    E2 = NE
    ns = 's'
    Surf = 'SouthInnerApproach'
    InnerApp(E1,E2,ns,Surf,accur,ApOls)
def InnerApp(E1,E2,ns,Surf,accur,ApOls):
    if accur >= 200:
        x = accur/100
    elif accur>=100 and accur< 200:
        x = accur / 20
    elif accur >=50 and accur< 100:
        x = accur / 15
    elif accur >0 and accur< 50:
        x = accur / 10
##    accur = x
    s = []
    Square = []
    count = 0
    ct = 0

    I = range(int(1+math.ceil((ApOls[4][0])/accur)))
    J = range(int(1+math.ceil((ApOls[4][2])/accur)))
    
    for i in I: 

        U = []
        T = []
        L=[]
        for j in J:
            par  = ApOls[4][1] + ApOls[4][2] - accur*j
            perp = ApOls[4][0]/2 - i*accur
            Z= (E1-RED)+(par - ApOls[3][1])*ApOls[4][3] 
          
            if par > ApOls[3][1]:
                if perp <= 0:
                    perp = 0
            if par <= ApOls[3][1]:
                par = ApOls[3][1]
                if perp <= 0:
                    perp = 0
                Z= (E1-RED)
          

            L.append([par,perp,Z])

        if perp == 0:
            T.append(i)
        if par == ApOls[3][1]:
            U.append(j)

        s.append(L)
        if len(U) > 0:
            J = range(U[0]+1)
        if len(T) > 0:
            I = range(T[0]+1)

    F = [1,-1]
    for n in range(2):
        f.write( '<Folder>\n')
        f.write( '<ScreenOverlay>\n')
        f.write( '<name>Runway: Code '+str(int(CN))+CL+NRunwayInfo+'</name>\n')
        f.write( '<visibility>0</visibility>\n')

        f.write('<overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n')
        f.write('<screenXY x="25" y="95" xunits="pixels" yunits="pixels"/>\n')
        f.write('<rotationXY x="0.5" y="0.5" xunits="fraction" yunits="fraction"/>\n')
        f.write('<size x="0" y="0" xunits="pixels" yunits="pixels"/>\n')	
        f.write('<styleUrl>#KMLStyler</styleUrl>\n')
        f.write('<ExtendedData>\n')				
        f.write('<SchemaData schemaUrl="#NewFeatureType">\n')
        f.write('<SimpleData name="Surface">Dimensions</SimpleData>\n')
        f.write('<SimpleData name="'+AppOLSNAME[2]+'">-</SimpleData>\n')
        for b in range(len(AppOLSDIMS[2])):
            f.write('<SimpleData name="'+AppOLSDIMS[2][b]+'">'+str(ApOls[2][b])+'</SimpleData>\n')

        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')
        OlsSurf = Surf+str(n+1)
        f.write( '<name>'+OlsSurf+'</name>\n')
        hero = []
        if n == 0 or n == 1:
            I = range(len(s))
        if n == 2 or n == 3:
            I = range(len(t))
        for i in I:
            if n == 0 or n == 1:
                bip = range(len(s[i]))
            if n == 2 or n == 3:
                bip = range(len(t[i]))
            for j in bip:            
                if i < max(I):
                    if n == 0 or n == 1:
                        bap = (len(s[i+1])-1)
                    if n == 2 or n == 3:
                        bap = (len(t[i+1])-1)
                    if j < bap:
                        xxx=[]
                        if n == 0: #adjacent to runway right
                            xx =[
                            [s[i][j][0]*F[1],    s[i][j][1]*F[0],        s[i][j][2]],
                            [s[i][j+1][0]*F[1],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[1],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[1],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                            [s[i][j][0]*F[1],    s[i][j][1]*F[0],        s[i][j][2]]
                            ]
                        if n == 1: #adjacent to runway left
                            xx =[
                            [s[i][j][0]*F[1],    s[i][j][1]*F[1],        s[i][j][2]],
                            [s[i][j+1][0]*F[1],  s[i][j+1][1]*F[1],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[1],s[i+1][j+1][1]*F[1],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[1],  s[i+1][j][1]*F[1],      s[i+1][j][2]],
                            [s[i][j][0]*F[1],    s[i][j][1]*F[1],        s[i][j][2]]
                            ]

                        f.write(   "<Placemark>\n")
                        f.write(   "<name>n="+str(n)+" i="+str(i)+" j="+str(j)+"</name>\n")  
                        f.write(   "<styleUrl>#m_ylw-pushpin</styleUrl>\n")
                        ##extended data
                        H = []
                        for h in range(len(xx)):
                            e = RED+xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],e,ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            H.append(Wgs[2])
                        Hn = min(H)
                        Hm = max(H)
                        f.write(   "<ExtendedData>")
                        f.write(   '<SchemaData schemaUrl="#S_t1_ISDDDDDDDDSSS">')
                        f.write(   '<SimpleData name="Surface">'+OlsSurf+'</SimpleData>')
                        f.write(   '<SimpleData name="Z-min">'+str(Hn)+'</SimpleData>')
                        f.write(   '<SimpleData name="Z-max">'+str(Hm)+'</SimpleData>')
                        f.write(   '</SchemaData>')    
                        f.write(   "</ExtendedData>")
                        ##extended data
                        
                        f.write(   "<Polygon>\n")
                        f.write(   "<altitudeMode>absolute</altitudeMode>\n")
                        f.write(   "<outerBoundaryIs>\n")
                        f.write(   "<LinearRing>\n")
                        f.write(   "<coordinates>\n")
                        
                        for h in range(len(xx)):
                            e = RED+xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],e,ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                            f.write(   "\n")
                      
                        f.write(   "</coordinates>\n")
                        f.write(   "</LinearRing>\n")
                        f.write(   "</outerBoundaryIs>\n"	)	
                        f.write(   "</Polygon>\n"	)		
                        f.write(   "</Placemark>\n")
        f.write( '</Folder>\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
