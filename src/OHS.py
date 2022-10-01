# -*- coding: cp1252 -*-
import sys
import os
import math
import OLSDims
import EnvSettings

from osgeo import osr
import mdl
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

def OHSSurf(ARPCoords,ApOlsARP,accur):
    ARPE=ARPCoords[0]
    ARPN=ARPCoords[1]
    ARPZ=ARPCoords[2]
    Z=ApOlsARP[0]
    R=ApOlsARP[1]
    Surf = 'OuterHorizontalSurface'
    ns = 'n'
    if accur >= 3000:
        x = accur/100
    elif accur>=1000 and accur< 3000:
        x = accur / 50
    elif accur >=100 and accur< 1000:
        x = accur / 20
    elif accur >0 and accur< 100:
        x = accur / 10
    s = []
    Square = []
    count = 0
    ct = 0

    I = range(int(1+math.ceil(R/accur)))
    J = range(int(1+math.ceil(2*math.pi*R/accur)))
    for i in I: 
        U = []
        T = []
        L = []
        for j in J:
            par = (R-i*accur)*(math.sin\
                     (\
                        math.radians\
                            (\
                                j*(360)/(2*math.pi*R/accur)\
                            )\
                      ))
            perp = (R-i*accur)*(math.cos\
                     (\
                        math.radians\
                            (\
                                j*(360)/(2*math.pi*R/accur)\
                            )\
                      ))
            if j > 3*(2*math.pi*R/accur)/4 and par >= (R-i*accur)*(math.sin(math.radians(0*(360)/(2*math.pi*R/accur)))):
                par = (R-i*accur)*(math.sin(math.radians(0*(360)/(2*math.pi*R/accur))))
                perp = (R-i*accur)*(math.cos\
                     (\
                        math.radians\
                            (\
                                0*(360)/(2*math.pi*R/accur)\
                            )\
                      ))
            L.append([par,perp,Z])

##        if perp == TransEdge:
##            T.append(i)
##        if par == RwyLen/2:
##            U.append(j)

        s.append(L)
        if len(U) > 0:
            J = range(U[0]+1)
        if len(T) > 0:
            I = range(T[0]+1)

    F = [1,-1]
    for n in range(1):
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
        f.write('<SimpleData name="'+AppOLSNAME[0]+'">-</SimpleData>\n')
        for b in range(len(AppOLSDIMS[0])):
            f.write('<SimpleData name="'+AppOLSDIMS[0][b]+'">'+str(ApOlsARP[b])+'</SimpleData>\n')

        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')
        OlsSurf = Surf
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
                        xx =[
                        [s[i][j][0]*F[0],    s[i][j][1]*F[0],        s[i][j][2]],
                        [s[i][j+1][0]*F[0],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                        [s[i+1][j+1][0]*F[0],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                        [s[i+1][j][0]*F[0],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                        [s[i][j][0]*F[0],    s[i][j][1]*F[0],        s[i][j][2]]
                        ]


                        f.write(   "<Placemark>\n")
                        f.write(   "<name>n="+str(n)+" i="+str(i)+" j="+str(j)+"</name>\n")  
                        f.write(   "<styleUrl>#m_ylw-pushpin</styleUrl>\n")
                        ##extended data
                        H = []
                        for h in range(len(xx)):
                            e = RED+xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARPZ,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
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
                            e = ARPZ+xx[h][2]
                            deltaE = (NTE-STE)
                            deltaN = (NTN-STN)
                            Utm = mdl.toUTM(ARPE,ARPN,ARPE+deltaE,ARPN+deltaN,ARPZ,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                            f.write(   "\n")

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
