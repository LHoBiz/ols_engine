# -*- coding: cp1252 -*-
import math
import OLSDims
import mdl
import EnvSettings
from osgeo import osr
ip = mdl.Data()
NTOL=ip.NTOL
STOL=ip.STOL
AppOLSNAME=OLSDims.AppDim.AppOLSNAME
AppOLSDIMS=OLSDims.AppDim.AppOLSDIMS
TOOLSNAME=OLSDims.TODim.TOOLSNAME
f=ip.f
ToOLS = OLSDims.TODim.ToOLS
AppOLSNAME=OLSDims.AppDim.AppOLSNAME
AppOLSDIMS=OLSDims.AppDim.AppOLSDIMS
NRunwayInfo=ip.NRunwayInfo
SRunwayInfo=ip.SRunwayInfo
NIns = ip.NIns
if NIns == 'Y':
    NPrc=ip.NPrc
    if NPrc <> 'N':
        NBLDist=ip.NBLDist

DayOnly = ip.CN
CL=ip.CL
RED=ip.RED
NMTOW5700kg = ip.NMTOW5700kg
NMTOW22700kg=ip.NMTOW22700kg
SMTOW5700kg = ip.SMTOW5700kg
SMTOW22700kg=ip.SMTOW22700kg

RPT = ip.RPT


SIns = ip.SIns
if SIns == 'Y':
    SPrc=ip.SPrc
    if SPrc <> 'N':
        SBLDist=ip.SBLDist
RPT = ip.RPT


RWY_WID=ip.RWY_WID
RSW=ip.RSW

NE=ip.NE
SE=ip.SE
NTE=ip.NTE
NTN=ip.NTN
STE=ip.STE
STN=ip.STN
ARP=ip.ARP
SE=ip.SE
NE=ip.NE
NTOAlt=ip.NTOAlt
STOAlt=ip.STOAlt
STOTurn15d=ip.STOTurn15d
NTOTurn15d=ip.NTOTurn15d
zone=ip.zone
KML_NAME=ip.KML_NAME
completeName=ip.completeName


RwyLen = math.sqrt((NTE-STE)*(NTE-STE) + (NTN-STN)*(NTN-STN))
NCLWY=ip.NCLWY
SCLWY=ip.SCLWY

Div = .05
Slope = .05


ApLen = 900
NCLWY=0
CN = 'ALA'
CL = 'NA'
NRunwayInfo = ['Take-off/Approach','Transitional','Runway strip width']
ToOls = [['Divergence','Slope','App/TO area length'],[Div,Slope,ApLen,RSW]]

def ApN(accur):
    accur = int(accur)
    Elev = NE
    J = range(1+int(math.ceil(ApLen/accur)))
    I = range(1+int(math.ceil(((ApLen*Div)+RSW/2)/accur)))
    s = []
    for i in I:
        K = []
        T = []
        for j in J:
            perp = Div*ApLen+(RSW/2)      -  i*accur     - j*accur*Div
            par = ApLen - j*accur
            if perp <= 0:
                perp = 0
            if par <= 0:
                par = 0
            Z = Elev + Slope*par
            K.append([par,perp,Z])
            if perp == 0:
                T.append(j)
        s.append(K)
        if len(T) > 0:
            J = range(T[0]+1)
    F = [1,-1]
    for n in range(2):
        #folder 
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
            
        f.write( '<Folder>\n')
        
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        
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
        f.write('<SimpleData name="'+NRunwayInfo[0]+'">-</SimpleData>\n')
        for b in range(len(ToOls)):
            f.write('<SimpleData name="'+ToOls[0][b]+'">'+str(ToOls[1][b])+'</SimpleData>\n')

        				
        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')

        if n == 0:
            f.write( '<name>North'+NRunwayInfo[0]+'1</name>\n')
            
               
        if n == 1:
            f.write( '<name>North'+NRunwayInfo[0]+'2</name>\n')
        hero = []
        
        I = range(len(s))
        for i in I:
            J = range(len(s[i]))
            for j in J:               
                if i < max(I):
                    if j < (len(s[i+1])-1):
    ##                    print 'flag1',(len(s[i+1])-1),j < (len(s[i+1])-1)


                        if n == 0:
                            xx =[
                            [s[i][j][0]*F[1],    s[i][j][1]*F[0],        s[i][j][2]],
                            [s[i][j+1][0]*F[1],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[1],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[1],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                            [s[i][j][0]*F[1],    s[i][j][1]*F[0],        s[i][j][2]]
                            ]
                            ns = 'n'
                        if n == 1:
                            xx =[
                            [s[i][j][0]*F[1],    s[i][j][1]*F[1],        s[i][j][2]],
                            [s[i][j+1][0]*F[1],  s[i][j+1][1]*F[1],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[1],s[i+1][j+1][1]*F[1],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[1],  s[i+1][j][1]*F[1],      s[i+1][j][2]],
                            [s[i][j][0]*F[1],    s[i][j][1]*F[1],        s[i][j][2]]
                            ]
                            ns = 'n'
                        f.write(   "<Placemark>\n")
                        f.write(   "<name>n="+str(n)+" i="+str(i)+" j="+str(j)+"</name>\n")  
                        f.write(   "<styleUrl>#m_ylw-pushpin</styleUrl>\n")
                        ##extended data
                        H = []
                        for h in range(len(xx)):
                            e = xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            H.append(Wgs[2])
                        Hn = min(H)
                        Hm = max(H)
                        f.write(   "<ExtendedData>")
                        f.write(   '<SchemaData schemaUrl="#S_t1_ISDDDDDDDDSSS">')
                        f.write(   '<SimpleData name="Surface">'+NRunwayInfo[0]+'</SimpleData>')
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
                            e = xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            H.append(Wgs[2])
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                            f.write(   "\n")

                        f.write(   "</coordinates>\n")
                        f.write(   "</LinearRing>\n")
                        f.write(   "</outerBoundaryIs>\n")   
                        
                        
                        f.write(   "</Polygon>\n")		
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
        f.write( '\n')

def ApS(accur):
    accur = int(accur)
    Elev = SE
    J = range(1+int(math.ceil(ApLen/accur)))
    I = range(1+int(math.ceil(((ApLen*Div)+RSW/2)/accur)))
    s = []
    for i in I:
        K = []
        T = []
        for j in J:
            perp = Div*ApLen+(RSW/2)      -  i*accur     - j*accur*Div
            par = ApLen - j*accur
            if perp <= 0:
                perp = 0
            if par <= 0:
                par = 0
            Z = Elev + Slope*par
            K.append([par,perp,Z])
            
            if perp == 0:
                T.append(j)
            
        s.append(K)
        
        if len(T) > 0:
            J = range(T[0]+1)
    F = [1,-1]
    for n in range(2):
        #folder 
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
            
        f.write( '<Folder>\n')
        
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        f.write( '\n')
        
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
        f.write('<SimpleData name="'+NRunwayInfo[0]+'">-</SimpleData>\n')
        for b in range(len(ToOls)):
            f.write('<SimpleData name="'+ToOls[0][b]+'">'+str(ToOls[1][b])+'</SimpleData>\n')

        				
        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')

        if n == 0:
            f.write( '<name>North'+NRunwayInfo[0]+'1</name>\n')
            
               
        if n == 1:
            f.write( '<name>North'+NRunwayInfo[0]+'2</name>\n')
        hero = []
        
        I = range(len(s))
        for i in I:
            J = range(len(s[i]))
            for j in J:               
                if i < max(I):
                    if j < (len(s[i+1])-1):
    ##                    print 'flag1',(len(s[i+1])-1),j < (len(s[i+1])-1)


                        if n == 0:
                            xx =[
                            [s[i][j][0]*F[1],    s[i][j][1]*F[0],        s[i][j][2]],
                            [s[i][j+1][0]*F[1],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[1],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[1],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                            [s[i][j][0]*F[1],    s[i][j][1]*F[0],        s[i][j][2]]
                            ]
                            ns = 's'
                        if n == 1:
                            xx =[
                            [s[i][j][0]*F[1],    s[i][j][1]*F[1],        s[i][j][2]],
                            [s[i][j+1][0]*F[1],  s[i][j+1][1]*F[1],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[1],s[i+1][j+1][1]*F[1],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[1],  s[i+1][j][1]*F[1],      s[i+1][j][2]],
                            [s[i][j][0]*F[1],    s[i][j][1]*F[1],        s[i][j][2]]
                            ]
                            ns = 's'
                        f.write(   "<Placemark>\n")
                        f.write(   "<name>n="+str(n)+" i="+str(i)+" j="+str(j)+"</name>\n")  
                        f.write(   "<styleUrl>#m_ylw-pushpin</styleUrl>\n")
                        ##extended data
                        H = []
                        for h in range(len(xx)):
                            e = xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            H.append(Wgs[2])
                        Hn = min(H)
                        Hm = max(H)
                        f.write(   "<ExtendedData>")
                        f.write(   '<SchemaData schemaUrl="#S_t1_ISDDDDDDDDSSS">')
                        f.write(   '<SimpleData name="Surface">'+NRunwayInfo[0]+'</SimpleData>')
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
                            e = xx[h][2]
                            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xx[h][0],xx[h][1],xx[h][2],ns)
                            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, e))
                            H.append(Wgs[2])
                            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                            f.write(   "\n")

                        f.write(   "</coordinates>\n")
                        f.write(   "</LinearRing>\n")
                        f.write(   "</outerBoundaryIs>\n")   
                        
                        
                        f.write(   "</Polygon>\n")		
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
        f.write( '\n')
