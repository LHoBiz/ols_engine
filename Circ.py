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
def getParPerp(line,aye,dim,StraightCurv):
    if line == 0: ## straight
        if aye == 0: ##category of aircraft
            extra = 1.5*1852
            parra=1.0*1852
        elif aye == 1:##category of aircraft
            extra = 2.0*1852
            parra=1.5*1852
        length = RwyLen+extra
    if line == 1:
        if aye == 0: ##category of aircraft
            extra = 1.5*1852
            if StraightCurv == 's':
                parra=0
            elif StraightCurv == 'c':
                parra=1.0*1852
        elif aye == 1:##category of aircraft
            extra = 2.0*1852
            if StraightCurv == 's':
                parra=0
            elif StraightCurv == 'c':
                parra=1.5*1852
        length = RwyLen+extra
    if dim == 'parr':
        return parra
    if dim == 'extr':
        return extra
    if dim == 'lenth':
        return length
def NCirc(accur):
    s = []
    StraightCurv = 's'
    Square = []
    count = 0
    ct = 0
    for aye in range(2): #cats
        for line in range(2): #in n out
            I = range(int(1+math.ceil(getParPerp(line,aye,'lenth',StraightCurv)/accur)))
            L = []
            for j in I:
                par = accur*j
                if par >= getParPerp(line,aye,'lenth',StraightCurv):
                    par = getParPerp(line,aye,'lenth',StraightCurv)
                perp = getParPerp(line,aye,'parr',StraightCurv)
                Z=NE
                L.append([par,perp,Z])
            s.append(L)
    t=[]
    StraightCurv = 'c'
    for aye in range(2):
        for line in range(2): #near or far       
            Curvs1 = 2*math.pi*(getParPerp(line,aye,'parr',StraightCurv)/2/2) / accur
            Curvs = range(1+int(math.ceil(Curvs1)))
            K = []
            for j in Curvs:
                angle=j*180/Curvs1
                if angle >= 180:
                    angle = 180
                if line == 0:
                    par = (getParPerp(line,aye,'parr',StraightCurv)/2)*(math.sin\
                             (\
                                math.radians\
                                    (\
                                        (-1)*angle\
                                    )\
                              ))
                elif line == 1:
                    par = getParPerp(line,aye,'lenth',StraightCurv) + (getParPerp(line,aye,'parr',StraightCurv)/2)*(math.sin\
                             (\
                                math.radians\
                                    (\
                                        angle\
                                    )\
                              ))
                if line == 0:
                    perp = math.sqrt(math.fabs((getParPerp(line,aye,'parr',StraightCurv)/2)*(getParPerp(line,aye,'parr',StraightCurv)/2)-par*par)) + getParPerp(line,aye,'parr',StraightCurv)/2
                    if angle >= 90:
                        perp = -1*math.sqrt(math.fabs((getParPerp(line,aye,'parr',StraightCurv)/2)*(getParPerp(line,aye,'parr',StraightCurv)/2)-par*par)) + getParPerp(line,aye,'parr',StraightCurv)/2

                elif line == 1:
                    perp = -1*math.sqrt(math.fabs((getParPerp(line,aye,'parr',StraightCurv)/2)*(getParPerp(line,aye,'parr',StraightCurv)/2)-(par- getParPerp(line,aye,'lenth',StraightCurv))*(par- getParPerp(line,aye,'lenth',StraightCurv)))) \
                           + getParPerp(line,aye,'parr',StraightCurv)/2
                    if angle >= 90:
                        perp = math.sqrt(math.fabs((getParPerp(line,aye,'parr',StraightCurv)/2)*(getParPerp(line,aye,'parr',StraightCurv)/2)-(par - getParPerp(line,aye,'lenth',StraightCurv))*(par - getParPerp(line,aye,'lenth',StraightCurv)))) \
                               + getParPerp(line,aye,'parr',StraightCurv)/2
                Z=NE
                K.append([par,perp,Z])
            t.append(K)
    F = [1,-1]
    for n in range(2):
        if n == 0:
            OlsSurf = 'Runway 30 Cat A / B Circuit'        
        if n == 1:
            OlsSurf = 'Runway 30 Cat C Circuit'
        f.write( '<Folder>\n')
        f.write( '<ScreenOverlay>\n')
        f.write( '<name>Runway: Code '+str(int(CN))+CL+NRunwayInfo+'</name>\n')
        f.write( '<visibility>0</visibility>\n')

        f.write('<overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n')
        f.write('<screenXY x="25" y="95" xunits="pixels" yunits="pixels"/>\n')
        f.write('<rotationXY x="0.5" y="0.5" xunits="fraction" yunits="fraction"/>\n')
        f.write('<size x="0" y="0" xunits="pixels" yunits="pixels"/>\n')	
        f.write('<styleUrl>#msn_ylw-pushpin</styleUrl>\n')
        f.write('<ExtendedData>\n')				
        f.write('<SchemaData schemaUrl="#NewFeatureType">\n')
        f.write('<SimpleData name="Surface">Dimensions</SimpleData>\n')
        f.write('<SimpleData name="'+OlsSurf+'">-</SimpleData>\n')
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


        f.write( '<name>'+OlsSurf+'</name>\n')
##        f.write('<open>1</open>\n')
        hero = []
        ns = 'n'
        xxx = [s,t]
        for l in range(len(xxx)):
            xx = xxx[l]
            for b in range(len(xx)):   
                f.write(   """<Placemark>
                        <name>Untitled Path</name>
                        <styleUrl>#msn_ylw-pushpin</styleUrl>
                        <LineString>
                                <tessellate>1</tessellate>
                                <coordinates>""")
                for h in range(len(xx[b])):
                    e = RED+xx[b][h][2]
                    Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[b][h][0],xx[b][h][1],xx[b][h][2],ns)
                    Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                    if n == 0:
                        if b == 0 or b == 1:
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                    if n == 1:
                        if b == 2 or b == 3:
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                    f.write(   "\n")
                f.write(   """</coordinates>
                        </LineString>
                </Placemark>""")
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
def SCirc(accur):
    s = []
    StraightCurv = 's'
    Square = []
    count = 0
    ct = 0
    for aye in range(2): #cats
        for line in range(2): #in n out
            I = range(int(1+math.ceil(getParPerp(line,aye,'lenth',StraightCurv)/accur)))
            L = []
            for j in I:
                par = accur*j
                if par >= getParPerp(line,aye,'lenth',StraightCurv):
                    par = getParPerp(line,aye,'lenth',StraightCurv)
                perp = getParPerp(line,aye,'parr',StraightCurv)
                perp = -1*perp
                Z=SE
                L.append([par,perp,Z])
            s.append(L)
    t=[]
    StraightCurv = 'c'
    for aye in range(2):
        for line in range(2): #near or far       
            Curvs1 = 2*math.pi*(getParPerp(line,aye,'parr',StraightCurv)/2/2) / accur
            Curvs = range(1+int(math.ceil(Curvs1)))
            K = []
            for j in Curvs:
                angle=j*180/Curvs1
                if angle >= 180:
                    angle = 180
                if line == 0:
                    par = (getParPerp(line,aye,'parr',StraightCurv)/2)*(math.sin\
                             (\
                                math.radians\
                                    (\
                                        (-1)*angle\
                                    )\
                              ))
                elif line == 1:
                    par = getParPerp(line,aye,'lenth',StraightCurv) + (getParPerp(line,aye,'parr',StraightCurv)/2)*(math.sin\
                             (\
                                math.radians\
                                    (\
                                        angle\
                                    )\
                              ))
                if line == 0:
                    perp = math.sqrt(math.fabs((getParPerp(line,aye,'parr',StraightCurv)/2)*(getParPerp(line,aye,'parr',StraightCurv)/2)-par*par)) + getParPerp(line,aye,'parr',StraightCurv)/2
                    if angle >= 90:
                        perp = -1*math.sqrt(math.fabs((getParPerp(line,aye,'parr',StraightCurv)/2)*(getParPerp(line,aye,'parr',StraightCurv)/2)-par*par)) + getParPerp(line,aye,'parr',StraightCurv)/2

                elif line == 1:
                    perp = -1*math.sqrt(math.fabs((getParPerp(line,aye,'parr',StraightCurv)/2)*(getParPerp(line,aye,'parr',StraightCurv)/2)-(par- getParPerp(line,aye,'lenth',StraightCurv))*(par- getParPerp(line,aye,'lenth',StraightCurv)))) \
                           + getParPerp(line,aye,'parr',StraightCurv)/2
                    if angle >= 90:
                        perp = math.sqrt(math.fabs((getParPerp(line,aye,'parr',StraightCurv)/2)*(getParPerp(line,aye,'parr',StraightCurv)/2)-(par - getParPerp(line,aye,'lenth',StraightCurv))*(par - getParPerp(line,aye,'lenth',StraightCurv)))) \
                               + getParPerp(line,aye,'parr',StraightCurv)/2
                perp = -1*perp
                Z=NE
                K.append([par,perp,Z])
            t.append(K)
    F = [1,-1]
    for n in range(2):
        if n == 0:
            OlsSurf = 'Runway 30 Cat A / B Circuit'        
        if n == 1:
            OlsSurf = 'Runway 30 Cat C Circuit'
        f.write( '<Folder>\n')
        f.write( '<ScreenOverlay>\n')
        f.write( '<name>Runway: Code '+str(int(CN))+CL+NRunwayInfo+'</name>\n')
        f.write( '<visibility>0</visibility>\n')

        f.write('<overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n')
        f.write('<screenXY x="25" y="95" xunits="pixels" yunits="pixels"/>\n')
        f.write('<rotationXY x="0.5" y="0.5" xunits="fraction" yunits="fraction"/>\n')
        f.write('<size x="0" y="0" xunits="pixels" yunits="pixels"/>\n')	
        f.write('<styleUrl>#msn_ylw-pushpin</styleUrl>\n')
        f.write('<ExtendedData>\n')				
        f.write('<SchemaData schemaUrl="#NewFeatureType">\n')
        f.write('<SimpleData name="Surface">Dimensions</SimpleData>\n')
        f.write('<SimpleData name="'+OlsSurf+'">-</SimpleData>\n')
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


        f.write( '<name>'+OlsSurf+'</name>\n')
##        f.write('<open>1</open>\n')
        hero = []
        ns = 's'
        xxx = [s,t]
        for l in range(len(xxx)):
            xx = xxx[l]
            for b in range(len(xx)):   
                f.write(   """<Placemark>
                        <name>Untitled Path</name>
                        <styleUrl>#msn_ylw-pushpin</styleUrl>
                        <LineString>
                                <tessellate>1</tessellate>
                                <coordinates>""")
                for h in range(len(xx[b])):
                    e = RED+xx[b][h][2]
                    Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[b][h][0],xx[b][h][1],xx[b][h][2],ns)
                    Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                    if n == 0:
                        if b == 0 or b == 1:
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                    if n == 1:
                        if b == 2 or b == 3:
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                    f.write(   "\n")
                f.write(   """</coordinates>
                        </LineString>
                </Placemark>""")
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
