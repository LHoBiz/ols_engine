# -*- coding: cp1252 -*-
import math
from . import OLSDims
from . import mdl
from . import EnvSettings
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

def NInHor(ApOls,accur):
    E1 = NE
    E2 = SE
    ns = 'n'
    Surf = 'NorthInnerHorizontal'
    InHor(E1,E2,ns,Surf,accur,ApOls)
def SInHor(ApOls,accur):
    E1 = SE
    E2 = NE
    ns = 's'
    Surf = 'SouthInnerHorizontal'
    InHor(E1,E2,ns,Surf,accur,ApOls)
def InHor(E1,E2,ns,Surf,accur,ApOls):
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

    I = range(int(1+math.ceil(ApOls[2][1]/accur)))
    J = range(int(1+math.ceil((ApOls[3][1]+(RwyLen/2))/accur)))
    for i in I: 

        U = []
        T = []
        L=[]
        for j in J:
            par = accur*j - ApOls[3][1]
            perp = ApOls[2][1] - i*accur
            Z=ApOls[2][0]
            TransEdge = RSW/2+(ApOls[2][0]+(RED-E1))/ApOls[5][0] + par*((E1-E2)/RwyLen/ApOls[5][0]) 
            TransEdge1= RSW/2+(ApOls[2][0]+(RED-E1))/ApOls[5][0] + ((j-1)*accur )*((E1-E2)/(RwyLen)/ApOls[5][0])
            
            if par < RwyLen/2:
                if perp <= TransEdge:
                    perp = TransEdge
            if par >= RwyLen/2:
                par = RwyLen/2
                par1 = (par-RwyLen/2)/accur
                Z=ApOls[2][0]
                if perp > TransEdge:
                    perp = ApOls[2][1] - i*accur
                if perp <= TransEdge:
                    perp = RSW/2+(ApOls[2][0]+(RED-E1))/ApOls[5][0] + RwyLen/2*((E1-E2)/RwyLen/ApOls[5][0])# - (TransEdge-TransEdge1)*par1
            L.append([par,perp,Z])

        if perp == TransEdge:
            T.append(i)
        if par == RwyLen/2:
            U.append(j)

        s.append(L)
        if len(U) > 0:
            J = range(U[0]+1)
        if len(T) > 0:
            I = range(T[0]+1)

    t=[]
    I = range(int(math.ceil(ApOls[2][1]/accur)+1))
    for i in I:
        Curvs1 = 2*math.pi*(ApOls[2][1])/4 / accur
        T = []
        K = []
        Curvs = range(1+int(math.ceil(Curvs1)))
        div = accur     
        for j in Curvs:
            x = ApOls[3][0]/2+((ApOls[2][0] +(RED-E1))/ApOls[5][0]) #  = perp of Outer Edge of Trans adjacent to NthTrsld
            if (ApOls[2][0] + (RED-E1))/ApOls[3][4] <= ApOls[3][3]:
                y = ApOls[3][0]/2+(ApOls[2][0] + (RED-E1))/ApOls[3][4] * ApOls[3][2] # = perp of TranMeetApp
            elif (ApOls[2][0] + (RED-E1))/ApOls[3][4] > ApOls[3][3]:
                y = ApOls[3][0]/2+(ApOls[3][3] + \
                           (\
                            (ApOls[2][0]-(ApOls[3][2]*ApOls[3][3])) +(RED-E1)\
                            )\
                           /ApOls[3][6] )* ApOls[3][2] # = perp of TranMeetApp    
            n1 = (x-y)/((ApOls[2][0] + (RED-E1))/ApOls[3][4])
            n2 = ApOls[3][2]
            L1 = (x-n1*j*accur) #change in perp outer line
            L2 = (ApOls[3][0]/2 + ApOls[3][2]*accur*j*(1)) # change in perp app outer line
            

            par = ApOls[3][1] + (ApOls[2][1]-i*div)*(math.sin\
                     (\
                        math.radians\
                            (\
                                j*(360/4)/Curvs1\
                            )\
                      ))
            if j*(360/4)/Curvs1 >= 90:
                par = ApOls[3][1] + (ApOls[2][1]-i*div)
            if par <=ApOls[3][1]:
                par = ApOls[3][1]
                
            perp=math.sqrt(math.fabs((ApOls[2][1] - i*div)*(ApOls[2][1] - i*div)-(par-ApOls[3][1])*(par-ApOls[3][1])))


            ##To snip IHS along the Transitional surface outer edge
##            if par > ParTransY and parUp <= ParTransY:
##                perp > PerpTransY and perp <= PerpTransY:
##                    par = 
                    
                    
            Z=ApOls[2][0]
            c = [par,perp,Z]
            K.append(c)

        t.append(K)
        if perp == 0 :
            U.append(j)
        if len(U) > 0:
            Curvs = range(U[0]+2)
    F = [1,-1]
    for n in range(4):
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
                            [s[i][j][0]*F[0],    s[i][j][1]*F[0],        s[i][j][2]],
                            [s[i][j+1][0]*F[0],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[0],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[0],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                            [s[i][j][0]*F[0],    s[i][j][1]*F[0],        s[i][j][2]]
                            ]
                        if n == 1: #adjacent to runway left
                            xx =[
                            [s[i][j][0]*F[0],    s[i][j][1]*F[1],        s[i][j][2]],
                            [s[i][j+1][0]*F[0],  s[i][j+1][1]*F[1],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[0],s[i+1][j+1][1]*F[1],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[0],  s[i+1][j][1]*F[1],      s[i+1][j][2]],
                            [s[i][j][0]*F[0],    s[i][j][1]*F[1],        s[i][j][2]]
                            ]
                        if n == 2: #converging parts right
                            xx =[
                            [t[i][j][0]*F[1],    t[i][j][1]*F[0],        t[i][j][2]],
                            [t[i][j+1][0]*F[1],  t[i][j+1][1]*F[0],      t[i][j+1][2]],
                            [t[i+1][j+1][0]*F[1],t[i+1][j+1][1]*F[0],    t[i+1][j+1][2]],
                            [t[i+1][j][0]*F[1],  t[i+1][j][1]*F[0],      t[i+1][j][2]],
                            [t[i][j][0]*F[1],    t[i][j][1]*F[0],        t[i][j][2]]
                            ]
                            if i > 0 and j==(len(t[i+1])-2) and (len(t[i-1])-1) > (len(t[i])-1) -1:
                                dif = ((len(t[i])-1)-(len(t[i+1])-1)  )
                                xxx = []
                                for d in range(dif):
                                    d1 = d+1
                                    xxx.append([
                                    [t[i+1][j+1][0]*F[1],    t[i+1][j+1][1]*F[0],        t[i+1][j+1][2]],
                                    [t[i][j+d1][0]*F[1],  t[i][j+d1][1]*F[0],      t[i][j+d1][2]],
                                    [t[i][j+1+d1][0]*F[1],t[i][j+1+d1][1]*F[0],    t[i][j+1+d1][2]],
                                    [t[i+1][j+1][0]*F[1],    t[i+1][j+1][1]*F[0],        t[i+1][j+1][2]],
                                    ])
                        if n == 3:#converging parts left
                            xx =[
                            [t[i][j][0]*F[1],    t[i][j][1]*F[1],        t[i][j][2]],
                            [t[i][j+1][0]*F[1],  t[i][j+1][1]*F[1],      t[i][j+1][2]],
                            [t[i+1][j+1][0]*F[1],t[i+1][j+1][1]*F[1],    t[i+1][j+1][2]],
                            [t[i+1][j][0]*F[1],  t[i+1][j][1]*F[1],      t[i+1][j][2]],
                            [t[i][j][0]*F[1],    t[i][j][1]*F[1],        t[i][j][2]]
                            ]
                            if i > 0 and j==(len(t[i+1])-2) and (len(t[i-1])-1) > (len(t[i])-1) -1:
                                dif = ((len(t[i])-1)-(len(t[i+1])-1)  )
                                xxx = []
                                for d in range(dif):
                                    d1 = d+1
                
                                    xxx.append([
                                    [t[i+1][j+1][0]*F[1],    t[i+1][j+1][1]*F[1],        t[i+1][j+1][2]],
                                    [t[i][j+d1][0]*F[1],  t[i][j+d1][1]*F[1],      t[i][j+d1][2]],
                                    [t[i][j+1+d1][0]*F[1],t[i][j+1+d1][1]*F[1],    t[i][j+1+d1][2]],
                                    [t[i+1][j+1][0]*F[1],    t[i+1][j+1][1]*F[1],        t[i+1][j+1][2]],
                                    ])
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
                        ##extended data
                        
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
                            
                        if len(xxx)>0:
                            for b in range(len(xxx)):
                                for h in range(len(xxx[b])):
                                    e = RED+xxx[b][h][2]
                                    Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,SE,NE,xxx[b][h][0],xxx[b][h][1],xxx[b][h][2],ns)
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
