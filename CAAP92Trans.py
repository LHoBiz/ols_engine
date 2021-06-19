# -*- coding: cp1252 -*-
import math
import OLSDims
import mdl
import EnvSettings
from osgeo import osr
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

Div = .05
Slope = .2


ApLen = 900
NCLWY=0
CN = 'ALA'
CL = 'NA'
NRunwayInfo = ['Take-off/Approach','Transitional','Runway strip width']
ToOls = [['Divergence','Slope','App/TO area length'],[Div,Slope,ApLen,RSW]]

LatExt = 45 + RSW/2
def ApTransN(accur):
    accur = int(accur)
    s = []
    Square = []
    count = 0
    ct = 0
    #The I and J for part adjacent to the runway strip.
    I = range(1+int(math.ceil((LatExt-(RSW/2))/(accur*(1-Slope)))))
    J = range(int(1+math.ceil((RwyLen/2)/accur)))
    for i in I:
        K = []
        U = []
        T = []
        for j in J:
            par  =   j*accur
            perp = LatExt - i*accur*(1-Slope)
            if par >= RwyLen/2:
                par = RwyLen/2
            if perp <= RSW/2:
                perp = RSW/2
            Z = (NE-RED) + (par)*(SE-NE)/RwyLen + (perp-RSW/2)*Slope
            K.append([par,perp,Z])
            if perp == RSW/2:
                T.append(i)
            if par == RwyLen/2:
                U.append(j)
        s.append(K)
        if len(U) > 0:
            J = range(U[0]+1)
        if len(T) > 0:
            I = range(T[0]+1)

    ## I and J for the adjacent part of the approach surface.
    t = []
    Square = []
    count = 0
    ct = 0

    D = []
    x = LatExt #  = perp of Outer Edge of Trans adjacent to NthTrsld
    y = RSW/2+(((LatExt-(RSW/2))*Slope )/.05 )* Div # = perp of TranMeetApp
    n1 = (x-y)/((LatExt-(RSW/2))*Slope /.05)
    n2 = Div
    I = range(1+int(math.ceil(x/(accur*(1-Slope)) )))
    J = range(int(1+math.ceil(\
        (((LatExt - RSW/2)/Div)/accur)\
        )))
    for i in I:
        K = []
        T = []
        for j in J:
           
            par = j*accur
            if par >= ((LatExt - RSW/2)/Div):
                par = ((LatExt - RSW/2)/Div)
            perp = x - accur*n1*j - i*(accur*(1-Slope))
            Z =(NE-RED) + (LatExt-(RSW/2))*Slope -  i*accur*(1-Slope)*(Slope)
            if perp <= (par*Div + RSW/2):
                perp = (par*Div + RSW/2)
                Z =(NE-RED) + par*0.05
            K.append([par,perp,Z])
            if perp == (par*Div + RSW/2):
                T.append(j)
        if len(T) > 0:
            J = range(T[0]+1)
        t.append(K)

    F = [1,-1]
    for n in range(4):
        f.write( '<Folder>\n')
        f.write( '<ScreenOverlay>\n')
        f.write( '<name>Runway: Code '+str(CN)+'</name>\n')
        f.write( '<visibility>0</visibility>\n')
	
        f.write('<overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n')
        f.write('<screenXY x="25" y="95" xunits="pixels" yunits="pixels"/>\n')
        f.write('<rotationXY x="0.5" y="0.5" xunits="fraction" yunits="fraction"/>\n')
        f.write('<size x="0" y="0" xunits="pixels" yunits="pixels"/>\n')	
        f.write('<styleUrl>#KMLStyler</styleUrl>\n')
        f.write('<ExtendedData>\n')				
        f.write('<SchemaData schemaUrl="#NewFeatureType">\n')
        f.write('<SimpleData name="Surface">Dimensions</SimpleData>\n')
        f.write('<SimpleData name="'+NRunwayInfo[1]+'">-</SimpleData>\n')
        for b in range(len(ToOls)):
            f.write('<SimpleData name="'+ToOls[0][b]+'">'+str(ToOls[1][b])+'</SimpleData>\n')

        				
        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        if n == 0:
            OlsSurf = 'NorthTransitional1'
        if n == 1:
            OlsSurf = 'NorthTransitional2'
        if n == 2:
            OlsSurf = 'NorthTransitional3'
        if n == 3:
            OlsSurf = 'NorthTransitional4'
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
                        if n == 0: #adjacent to runway right
                            xx =[
                            [s[i][j][0]*F[0],    s[i][j][1]*F[0],        s[i][j][2]],
                            [s[i][j+1][0]*F[0],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[0],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[0],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                            [s[i][j][0]*F[0],    s[i][j][1]*F[0],        s[i][j][2]]
                            ]
                            ns = 'n'
                        if n == 1: #adjacent to runway left
                            xx =[
                            [s[i][j][0]*F[0],    s[i][j][1]*F[1],        s[i][j][2]],
                            [s[i][j+1][0]*F[0],  s[i][j+1][1]*F[1],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[0],s[i+1][j+1][1]*F[1],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[0],  s[i+1][j][1]*F[1],      s[i+1][j][2]],
                            [s[i][j][0]*F[0],    s[i][j][1]*F[1],        s[i][j][2]]
                            ]
                            ns = 'n'
                        if n == 2: #converging parts right
                            
                            xx =[
                            [t[i][j][0]*F[1],    t[i][j][1]*F[0],        t[i][j][2]],
                            [t[i][j+1][0]*F[1],  t[i][j+1][1]*F[0],      t[i][j+1][2]],
                            [t[i+1][j+1][0]*F[1],t[i+1][j+1][1]*F[0],    t[i+1][j+1][2]],
                            [t[i+1][j][0]*F[1],  t[i+1][j][1]*F[0],      t[i+1][j][2]],
                            [t[i][j][0]*F[1],    t[i][j][1]*F[0],        t[i][j][2]]
                            ]
                            ns = 'n'
                        if n == 3:#converging parts left
                            xx =[
                            [t[i][j][0]*F[1],    t[i][j][1]*F[1],        t[i][j][2]],
                            [t[i][j+1][0]*F[1],  t[i][j+1][1]*F[1],      t[i][j+1][2]],
                            [t[i+1][j+1][0]*F[1],t[i+1][j+1][1]*F[1],    t[i+1][j+1][2]],
                            [t[i+1][j][0]*F[1],  t[i+1][j][1]*F[1],      t[i+1][j][2]],
                            [t[i][j][0]*F[1],    t[i][j][1]*F[1],        t[i][j][2]]
                            ]
                            ns = 'n'
                        f.write(   "<Placemark>\n")
                        f.write(   "<name>n="+str(n)+" i="+str(i)+" j="+str(j)+"</name>\n")  
                        f.write(   "<styleUrl>#m_ylw-pushpin</styleUrl>\n")
                        ##extended data
                        H = []
                        for h in range(len(xx)):
                            e = RED+xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
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
                        f.write(   "<Polygon>\n")
                        f.write(   "<altitudeMode>absolute</altitudeMode>\n")
                        f.write(   "<outerBoundaryIs>\n")
                        f.write(   "<LinearRing>\n")
                        f.write(   "<coordinates>\n")
                        for h in range(len(xx)):
                            e = RED+xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                            f.write(   "\n")
                        f.write(   "</coordinates>\n")
                        f.write(   "</LinearRing>\n")
                        f.write(   "</outerBoundaryIs>\n"	)	
                        f.write(   "</Polygon>\n"	)		
                        f.write(   "</Placemark>\n")
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '</Folder>\n')
            
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
def ApTransS(accur):
    accur = int(accur)
    s = []
    Square = []
    count = 0
    ct = 0
    #The I and J for part adjacent to the runway strip.
    I = range(1+int(math.ceil((LatExt-(RSW/2))/(accur*(1-Slope)))))
    J = range(int(1+math.ceil((RwyLen/2)/accur)))
    for i in I:
        K = []
        U = []
        T = []
        for j in J:
            par  =   j*accur
            perp = LatExt - i*accur*(1-Slope)
            if par >= RwyLen/2:
                par = RwyLen/2
            if perp <= RSW/2:
                perp = RSW/2
            Z = (SE-RED) + (par)*(NE-SE)/RwyLen + (perp-RSW/2)*Slope
            K.append([par,perp,Z])
            if perp == RSW/2:
                T.append(i)
            if par == RwyLen/2:
                U.append(j)
        s.append(K)
        if len(U) > 0:
            J = range(U[0]+1)
        if len(T) > 0:
            I = range(T[0]+1)

    ## I and J for the adjacent part of the approach surface.
    t = []
    Square = []
    count = 0
    ct = 0

    D = []
    x = LatExt #  = perp of Outer Edge of Trans adjacent to NthTrsld
    y = RSW/2+(((LatExt-(RSW/2))*Slope )/.05 )* Div # = perp of TranMeetApp
    n1 = (x-y)/((LatExt-(RSW/2))*Slope /.05)
    n2 = Div
    I = range(1+int(math.ceil(x/(accur*(1-Slope)) )))
    J = range(int(1+math.ceil(\
        (((LatExt - RSW/2)/Div)/accur)\
        )))
    for i in I:
        K = []
        T = []
        for j in J:
           
            par = j*accur
            if par >= ((LatExt - RSW/2)/Div):
                par = ((LatExt - RSW/2)/Div)
            perp = x - accur*n1*j - i*(accur*(1-Slope))
            Z =(SE-RED) + (LatExt-(RSW/2))*Slope -  i*accur*(1-Slope)*(Slope)
            if perp <= (par*Div + RSW/2):
                perp = (par*Div + RSW/2)
                Z =(SE-RED) + par*0.05
            K.append([par,perp,Z])
            if perp == (par*Div + RSW/2):
                T.append(j)
        if len(T) > 0:
            J = range(T[0]+1)
        t.append(K)

    F = [1,-1]
    for n in range(4):
        f.write( '<Folder>\n')
        f.write( '<ScreenOverlay>\n')
        f.write( '<name>Runway: Code '+str(CN)+'</name>\n')
        f.write( '<visibility>0</visibility>\n')
	
        f.write('<overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n')
        f.write('<screenXY x="25" y="95" xunits="pixels" yunits="pixels"/>\n')
        f.write('<rotationXY x="0.5" y="0.5" xunits="fraction" yunits="fraction"/>\n')
        f.write('<size x="0" y="0" xunits="pixels" yunits="pixels"/>\n')	
        f.write('<styleUrl>#KMLStyler</styleUrl>\n')
        f.write('<ExtendedData>\n')				
        f.write('<SchemaData schemaUrl="#NewFeatureType">\n')
        f.write('<SimpleData name="Surface">Dimensions</SimpleData>\n')
        f.write('<SimpleData name="'+NRunwayInfo[1]+'">-</SimpleData>\n')
        for b in range(len(ToOls)):
            f.write('<SimpleData name="'+ToOls[0][b]+'">'+str(ToOls[1][b])+'</SimpleData>\n')

        				
        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        if n == 0:
            OlsSurf = 'NorthTransitional1'
        if n == 1:
            OlsSurf = 'NorthTransitional2'
        if n == 2:
            OlsSurf = 'NorthTransitional3'
        if n == 3:
            OlsSurf = 'NorthTransitional4'
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
                        if n == 0: #adjacent to runway right
                            xx =[
                            [s[i][j][0]*F[0],    s[i][j][1]*F[0],        s[i][j][2]],
                            [s[i][j+1][0]*F[0],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[0],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[0],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                            [s[i][j][0]*F[0],    s[i][j][1]*F[0],        s[i][j][2]]
                            ]
                            ns = 's'
                        if n == 1: #adjacent to runway left
                            xx =[
                            [s[i][j][0]*F[0],    s[i][j][1]*F[1],        s[i][j][2]],
                            [s[i][j+1][0]*F[0],  s[i][j+1][1]*F[1],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[0],s[i+1][j+1][1]*F[1],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[0],  s[i+1][j][1]*F[1],      s[i+1][j][2]],
                            [s[i][j][0]*F[0],    s[i][j][1]*F[1],        s[i][j][2]]
                            ]
                            ns = 's'
                        if n == 2: #converging parts right
                            
                            xx =[
                            [t[i][j][0]*F[1],    t[i][j][1]*F[0],        t[i][j][2]],
                            [t[i][j+1][0]*F[1],  t[i][j+1][1]*F[0],      t[i][j+1][2]],
                            [t[i+1][j+1][0]*F[1],t[i+1][j+1][1]*F[0],    t[i+1][j+1][2]],
                            [t[i+1][j][0]*F[1],  t[i+1][j][1]*F[0],      t[i+1][j][2]],
                            [t[i][j][0]*F[1],    t[i][j][1]*F[0],        t[i][j][2]]
                            ]
                            ns = 's'
                        if n == 3:#converging parts left
                            xx =[
                            [t[i][j][0]*F[1],    t[i][j][1]*F[1],        t[i][j][2]],
                            [t[i][j+1][0]*F[1],  t[i][j+1][1]*F[1],      t[i][j+1][2]],
                            [t[i+1][j+1][0]*F[1],t[i+1][j+1][1]*F[1],    t[i+1][j+1][2]],
                            [t[i+1][j][0]*F[1],  t[i+1][j][1]*F[1],      t[i+1][j][2]],
                            [t[i][j][0]*F[1],    t[i][j][1]*F[1],        t[i][j][2]]
                            ]
                            ns = 's'
                        f.write(   "<Placemark>\n")
                        f.write(   "<name>n="+str(n)+" i="+str(i)+" j="+str(j)+"</name>\n")  
                        f.write(   "<styleUrl>#m_ylw-pushpin</styleUrl>\n")
                        ##extended data
                        H = []
                        for h in range(len(xx)):
                            e = RED+xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
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
                        f.write(   "<Polygon>\n")
                        f.write(   "<altitudeMode>absolute</altitudeMode>\n")
                        f.write(   "<outerBoundaryIs>\n")
                        f.write(   "<LinearRing>\n")
                        f.write(   "<coordinates>\n")
                        for h in range(len(xx)):
                            e = RED+xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                            f.write(   "\n")
                        f.write(   "</coordinates>\n")
                        f.write(   "</LinearRing>\n")
                        f.write(   "</outerBoundaryIs>\n"	)	
                        f.write(   "</Polygon>\n"	)		
                        f.write(   "</Placemark>\n")
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '</Folder>\n')
            
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
