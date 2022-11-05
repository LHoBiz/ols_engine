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

def NInTrans(ApOls,accur):
    E1 = NE
    E2 = SE
    ns = 'n'
    Surf = 'NorthInnerTransitional'
    
    s = ITransAdjToRwy(E1,E2,Surf,accur,ApOls)
    a = 0
    KMLWriter(ApOls,Surf,s,a,ns)
    
    s = ITransAdjToIApp(E1,E2,Surf,accur,ApOls)
    a = 1 
    KMLWriter(ApOls,Surf,s,a,ns)

    s = ITransAdjToBaulk(E1,E2,Surf,accur,ApOls)
    a = 0
    KMLWriter(ApOls,Surf,s,a,ns)
    
    
def SInTrans(ApOls,accur):
    E1 = SE
    E2 = NE
    ns = 's'
    Surf = 'SouthInnerTransitional'
    
    s = ITransAdjToRwy(E1,E2,Surf,accur,ApOls)
    a = 0
    KMLWriter(ApOls,Surf,s,a,ns)
    
    s = ITransAdjToIApp(E1,E2,Surf,accur,ApOls)
    a = 1
    KMLWriter(ApOls,Surf,s,a,ns)

    s = ITransAdjToBaulk(E1,E2,Surf,accur,ApOls)
    a = 0
    KMLWriter(ApOls,Surf,s,a,ns)
    
def ITransAdjToBaulk(E1,E2,Surf,accur,ApOls):
    ## I and J for the adjacent part of the approach surface.
    t = []
    Square = []
    count = 0
    ct = 0
    BlkOut = ApOls[7][1] + ((RED+ApOls[2][0]) - (E1+((E2-E1)/RwyLen)*ApOls[7][1]))/ApOls[7][3]
    x = ApOls[7][0]/2+(ApOls[2][0]+(RED-E1))/ApOls[6][0] + (ApOls[7][1])*((E1-E2)/RwyLen/ApOls[6][0]) - 0*accur*(1-ApOls[6][0])
    #  = perp of Outer Edge of Trans adjacent to inerBaulk
    #y = ApOls[7][0]/2 + ((RED+ApOls[2][0]) - (E1-RED) +((E2-E1)/RwyLen)*ApOls[7][1])/ApOls[6][0] # = perp of outer baulk
    y = ApOls[7][0]/2 + ((\
                BlkOut\
                        )\
                         -ApOls[7][1])*ApOls[7][2] 

    n1 = (x-y)/(BlkOut-ApOls[7][1])##Rate of change of perp of the line from outer InTrans at Ths to outer InTrans at Baulked outer edge
    n2 = ApOls[7][2]
    I = range(int(1+math.ceil(( (((RED+ApOls[2][0]) - ((E2-E1)/RwyLen)*ApOls[7][1]))/ApOls[7][2])/accur)))
    J = range(int(1+math.ceil( (((RED+ApOls[2][0]) - ((E2-E1)/RwyLen)*ApOls[7][1])/ApOls[7][3])/accur)))
    D = []
    for i in I:
        K = []
        T = []
        for j in J:
            L1 = (x-n1*j*accur) #change in perp outer line
            L2 = (ApOls[7][0]/2 + ApOls[7][2]*j*accur) # change in perp Baulked outer line
            par = accur*j + ApOls[7][1]
            perp = x - (par-ApOls[7][1])*accur*n1*j - i*accur*(1-ApOls[6][0])
            Z = (ApOls[2][0]) - i*accur*(1-ApOls[6][0])*ApOls[6][0]
            if par < BlkOut:
                par = par
                perp = L1 -  i*accur*(1-ApOls[6][0])
                Z = (ApOls[2][0]) - (L1-perp)*ApOls[6][0]#(ApOls[2][0]) - i*accur*(1-ApOls[6][0])*ApOls[6][0]
                if j == 0 and  perp <= L2:
                    Z = ((E2-E1)/RwyLen)*ApOls[7][1] + E1
                if perp <= L2:
                    par = par
                    perp = L2
                    Z =  ((E1-RED) +((E2-E1)/RwyLen)*ApOls[7][1]) + (par-ApOls[7][1])*ApOls[7][3]
                c = [par,perp,Z]
            if par >= BlkOut:
                par = BlkOut
                perp =y
##                Z = Z
                if perp <= L2:
                    par = BlkOut
                    parSup = ApOls[7][1] - accur*0  + BlkOut
                    perp = ApOls[7][0]/2 + (par-ApOls[7][1])*ApOls[7][2]
##                    Z =  accur*j*ApOls[7][3]- (RED-E1)
                Z = ((E1-RED) +((E2-E1)/RwyLen)*ApOls[7][1]) + (par-ApOls[7][1])*ApOls[7][3]
                c = [par,perp,Z]
            K.append(c)
            if perp == L2 :
                T.append(j)
            sq = [c[0],c[1]]
            Square.append(sq)
        if len(T) > 0:
            J = range(T[0]+1)
            sq = [c[0],c[1]]
            Square.append(sq)
        t.append(K)
    return t
        
def ITransAdjToIApp(E1,E2,Surf,accur,ApOls):
    ## I and J for the adjacent part of the approach surface.
    t = []
    Square = []
    count = 0
    ct = 0
    x = ApOls[4][0]/2+((ApOls[2][0] +(RED-E1))/ApOls[6][0]) #  = perp of Outer Edge of Trans adjacent to NthTrsld
    y = ApOls[4][0]/2+( ApOls[2][0] +(RED-E1) - ApOls[4][2]*ApOls[4][3])/ApOls[6][0]# = perp of TranMeetApp

    
    n1 = (x-y)/ApOls[4][2] ##Rate of change of the line from outer InTrans at Ths to outer InTrans at InApp outer edge
    n2 = ApOls[4][0]/2
    I = range(int(1+math.ceil(x/accur)))
    J = range(int(1+math.ceil(ApOls[4][2] /accur)))
    D = []
    for i in I:
        K = []
        T = []
        for j in J:
            par = accur*j + ApOls[4][1]  
            perp = x - accur*n1*j - i*accur*(1-ApOls[6][0])
            Z = ApOls[2][0] - i*accur*(1-ApOls[6][0])*ApOls[6][0]
            L1 = (x-n1*j*accur) #change in perp outer line
            L2 = (ApOls[4][0]/2 ) # change in perp app outer line
            if par > ApOls[4][1]:
                if perp >= L1 and perp > L2 and L1>L2:
                    par = par
                    perp =L1
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
                if perp < L1 and perp > L2:
                    par = par
                    perp = perp
                    Z = Z
                    c = [par,perp,Z]
                if perp < L1 and perp <= L2 and L1>L2:
                    par = par
                    perp = L2
                    Z =  accur*j*ApOls[4][3]- (RED-E1)
                    c = [par,perp,Z]
                if perp == L1 and perp == L2:
                    par = (ApOls[2][0] + (RED-E1))/ApOls[4][3]+ ApOls[4][1]
                    perp = y
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
                if L2> L1:
                    par = (ApOls[2][0] + (RED-E1))/ApOls[4][3]+ ApOls[4][1]
                    perp = y
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
            if par <= ApOls[4][1]:
                if perp < L1 and perp > L2:
                    par = ApOls[4][1]
                    perp = perp
                    Z = Z
                    c = [par,perp,Z]
                if perp >= L1 and perp > L2 and L1>L2:
                    par = ApOls[4][1]
                    perp =L1
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
                if perp < L1 and perp <= L2 and L1>L2:
                    par = ApOls[4][1]
                    perp = ApOls[4][0]/2
                    Z = (E1-RED)
                    c = [par,perp,Z]
            K.append(c)
            if perp == L2 :
                T.append(j)
            sq = [c[0],c[1]]
            Square.append(sq)
        if len(T) > 0:
            J = range(T[0]+1)
            sq = [c[0],c[1]]
            Square.append(sq)
        t.append(K)
    return t
    
def ITransAdjToRwy(E1,E2,Surf,accur,ApOls):
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
    
    #The I and J for part adjacent to the runway strip.
    I = range(int(1+math.ceil( max((ApOls[2][0]+(RED-E1))/ApOls[6][0],(ApOls[2][0]-((E1-E2)/2))/ApOls[5][0])/((1-ApOls[5][0])*accur))))
    J = range(int(1+math.ceil((ApOls[7][1] + ApOls[4][1])/accur)))
    for i in I:
        K = []
        U = []
        T = []
        for j in J:
            par  =   j*accur - ApOls[3][1]
            par1 = (j-1)*accur - ApOls[3][1] 
            par2 = (j+1)*accur - ApOls[3][1] ###marry trans with IHS  
            if par <= 0:
                perp =  ApOls[4][0]/2+(ApOls[2][0]+(RED-E1))/ApOls[6][0] - i*accur*(1-ApOls[6][0])
            elif par > 0:
                perp =  ApOls[4][0]/2+(ApOls[2][0]+(RED-E1))/ApOls[6][0] + (j*accur - ApOls[3][1])*((E1-E2)/RwyLen/ApOls[6][0]) - i*accur*(1-ApOls[6][0])                
            Z    =   ApOls[2][0]-i*accur*(1-ApOls[6][0])*ApOls[6][0]
            if par <  ApOls[7][1]  and par<= 0 and par <= - ApOls[3][1] and perp<=ApOls[4][0]/2:
                par = - ApOls[3][1]
                perp = ApOls[4][0]/2
                Z = (E1-RED) 
                c = [par,perp,Z]
            if par <  ApOls[7][1]  and par<= 0 and par <= - ApOls[3][1] and perp > ApOls[4][0]/2:
                par = - ApOls[3][1]
                perp = perp
                Z = Z
                c = [par,perp,Z]
            if par <  ApOls[7][1]  and par<= 0 and par > - ApOls[3][1] and perp <= ApOls[4][0]/2:
                par = par
                perp = ApOls[4][0]/2
                Z = (E1-RED) 
                c = [par,perp,Z]
            if par <  ApOls[7][1]  and par<= 0 and par > - ApOls[3][1] and perp > ApOls[4][0]/2:
                par = par
                perp = perp
                Z = Z
                c = [par,perp,Z]

            if par <  ApOls[7][1]  and par > 0 and perp > ApOls[4][0]/2: 
                par = par
                perp = perp
                Z = Z
                c = [par,perp,Z]
            if par <  ApOls[7][1]  and par > 0 and perp <= ApOls[4][0]/2:
                par = par
                perp = ApOls[4][0]/2
                Z = (E1-RED) + (j*accur -ApOls[3][1]) *(E2-E1)/RwyLen
                c = [par,perp,Z]
            if par >=  ApOls[7][1] and perp <= ApOls[4][0]/2:
                par = ApOls[7][1] 
                perp = ApOls[4][0]/2
                Z = (E1-RED) +((E2-E1)/RwyLen)*ApOls[7][1]
                c = [par,perp,Z]
            if par >=  ApOls[7][1]  and perp > ApOls[4][0]/2:
                par =  ApOls[7][1] 
                perp = ApOls[4][0]/2+(ApOls[2][0]+(RED-E1))/ApOls[6][0] + par*((E1-E2)/RwyLen/ApOls[6][0]) - i*accur*(1-ApOls[6][0])#perp
                Z = Z
                c = [par,perp,Z]
            K.append(c)
            if perp == ApOls[4][0]/2:
                T.append(i)
            if par ==  ApOls[7][1] :
                U.append(j)
            sq = [c[0],c[1]]
            Square.append(sq)
        s.append(K)
        if len(U) > 0:
            J = range(U[0]+1)
        if len(T) > 0:
            I = range(T[0]+1)
    return s
            
def KMLWriter(ApOls,Surf,s,a,ns):
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
                            [s[i][j][0]*F[a],    s[i][j][1]*F[0],        s[i][j][2]],
                            [s[i][j+1][0]*F[a],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[a],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[a],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                            [s[i][j][0]*F[a],    s[i][j][1]*F[0],        s[i][j][2]]
                            ]
                        if n == 1: #adjacent to runway left
                            xx =[
                            [s[i][j][0]*F[a],    s[i][j][1]*F[1],        s[i][j][2]],
                            [s[i][j+1][0]*F[a],  s[i][j+1][1]*F[1],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[a],s[i+1][j+1][1]*F[1],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[a],  s[i+1][j][1]*F[1],      s[i+1][j][2]],
                            [s[i][j][0]*F[a],    s[i][j][1]*F[1],        s[i][j][2]]
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
