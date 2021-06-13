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

def NorthTrans(ApOls,accur):
    E1 = NE
    E2 = SE
    ns = 'n'
    Surf = 'NorthTransitional'
    TransSurf(E1,E2,ns,Surf,accur,ApOls)
def SouthTrans(ApOls,accur):
    E1 = SE
    E2 = NE
    ns = 's'
    Surf = 'SouthTransitional'
    TransSurf(E1,E2,ns,Surf,accur,ApOls)


def TransSurf(E1,E2,ns,Surf,accur,ApOls):
    s = []
    Square = []
    count = 0
    ct = 0
    #The I and J for part adjacent to the runway strip.
    if E1 > E2:
        I = range(int(2+math.ceil(   (ApOls[2][0]+(RED-E1))/ApOls[5][0])/((1-ApOls[5][0])*accur)))
    if E1 <= E2:
        I = range(int(2+math.ceil(   (ApOls[2][0]+(RED-E1))/ApOls[5][0])/((1-ApOls[5][0])*accur)))


    J = range(int(1+math.ceil((RwyLen/2 + ApOls[3][1])/accur)))
    for i in I:
        K = []
        U = []
        T = []
        for j in J:
            par  =   j*accur - ApOls[3][1]
            par1 = (j-1)*accur - ApOls[3][1] ###incorporate these to 
            par2 = (j+1)*accur - ApOls[3][1] ###marry trans with IHS  - do with south too
            if par >= -ApOls[3][1] and  par <= 0:
                perp =  RSW/2+(ApOls[2][0]+(RED-E1))/ApOls[5][0]  - i*accur*(1-ApOls[5][0])
            if par > 0:
                perp =  RSW/2+(ApOls[2][0]+(RED-E1))/ApOls[5][0] + (par)*((E1-E2)/RwyLen/ApOls[5][0]) - i*accur*(1-ApOls[5][0])

            Z = ApOls[2][0]-i*accur*(1-ApOls[5][0])*ApOls[5][0]
             
            if par < RwyLen/2 and par<= 0 and par <= - ApOls[3][1] and perp<=RSW/2:
                par = - ApOls[3][1]
                perp = RSW/2
                Z = (E1-RED) 
                c = [par,perp,Z]
                K.append(c)
                if par2 > 0 and par < 0:
                    par = 0
                    perp = perp
                    Z = Z 
                    c = [par,perp,Z]
                    K.append(c)
            if par < RwyLen/2 and par<= 0 and par <= - ApOls[3][1] and perp > RSW/2:
                par = - ApOls[3][1]
                perp = perp
                Z = Z
                c = [par,perp,Z]
                K.append(c)
                if par2 > 0 and par < 0:
                    par = 0
                    perp = perp
                    Z = Z 
                    c = [par,perp,Z]
                    K.append(c)
            if par < RwyLen/2 and par<= 0 and par > - ApOls[3][1] and perp <= RSW/2:
                par = par
                perp = RSW/2
                Z = (E1-RED) 
                c = [par,perp,Z]
                K.append(c)
                if par2 > 0:
                    par = 0
                    perp = RSW/2
                    Z = (E1-RED) 
                    c = [par,perp,Z]
                    K.append(c)
            if par < RwyLen/2 and par<= 0 and par > - ApOls[3][1] and perp > RSW/2:
                par = par
                perp = perp
                Z = Z
                c = [par,perp,Z]
                K.append(c)
                if par2 > 0:
                    par = 0
                    perp = perp
                    Z = Z
                    c = [par,perp,Z]
                    K.append(c)

            if par < RwyLen/2 and par > -ApOls[3][1] and perp > RSW/2: 
                par = par
                perp = perp
                Z = Z
                c = [par,perp,Z]
                K.append(c)
                if par2 > 0 and par < 0:
                    par = 0
                    perp = perp
                    Z = Z 
                    c = [par,perp,Z]
                    K.append(c)
            if par < RwyLen/2 and par > -ApOls[3][1] and perp <= RSW/2:
                par = par
                perp = RSW/2
                Z = (E1-RED) + (j*accur -ApOls[3][1]) *(E2-E1)/RwyLen
                c = [par,perp,Z]
                K.append(c)
                if par2 > 0 and par < 0:
                    par = 0
                    perp = perp
                    Z = Z 
                    c = [par,perp,Z]
                    K.append(c)
            if par >= RwyLen/2 and perp <= RSW/2:
                par = RwyLen/2
                perp = RSW/2
                Z = (E1-RED) + (E2-E1)/2
                c = [par,perp,Z]
                K.append(c)
            if par >= RwyLen/2 and perp > RSW/2:
                par = RwyLen/2
                perp = RSW/2+(ApOls[2][0]+(RED-E1))/ApOls[5][0] + par*((E1-E2)/RwyLen/ApOls[5][0]) - i*accur*(1-ApOls[5][0])#perp
                Z = Z
                c = [par,perp,Z]
                K.append(c)
            if perp == RSW/2:
                T.append(i)
            if par == RwyLen/2:
                U.append(j)
            sq = [c[0],c[1]]
            Square.append(sq)
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
    I = range(int(1+math.ceil(x/accur)))
    J = range(int(1+math.ceil(\
       (((ApOls[2][0] + (RED-E1))/ApOls[3][4]))/accur\
        )))
    D = []
    for i in I:
        K = []
        T = []
        for j in J:
            par = accur*j + ApOls[3][1]  
            perp = x - accur*n1*j - i*accur*(1-ApOls[5][0])
            Z = ApOls[2][0] - i*accur*(1-ApOls[5][0])*ApOls[5][0]
            L1 = (x-n1*j*accur) #change in perp outer line
            L2 = (ApOls[3][0]/2 + ApOls[3][2]*accur*j*(1)) # change in perp app outer line
            if par > ApOls[3][1]:
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
                    Z =  accur*j*ApOls[3][4]- (RED-E1)
                    c = [par,perp,Z]
                if perp == L1 and perp == L2:
                    par = (ApOls[2][0] + (RED-E1))/ApOls[3][4]+ ApOls[3][1]
                    perp = y
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
                if L2> L1:
                    par = (ApOls[2][0] + (RED-E1))/ApOls[3][4]+ ApOls[3][1]
                    perp = y
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
            if par <= ApOls[3][1]:
                if perp < L1 and perp > L2:
                    par = ApOls[3][1]
                    perp = perp
                    Z = Z
                    c = [par,perp,Z]
                if perp >= L1 and perp > L2 and L1>L2:
                    par = ApOls[3][1]
                    perp =L1
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
                if perp < L1 and perp <= L2 and L1>L2:
                    par = ApOls[3][1]
                    perp = ApOls[3][0]/2
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
        f.write('<SimpleData name="'+AppOLSNAME[5]+'">-</SimpleData>\n')
        for b in range(len(AppOLSDIMS[5])):
            f.write('<SimpleData name="'+AppOLSDIMS[5][b]+'">'+str(ApOls[5][b])+'</SimpleData>\n')

        				
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
                           
                        if n == 3:#converging parts left
                            xx =[
                           [t[i][j][0]*F[1],    t[i][j][1]*F[1],        t[i][j][2]],
                            [t[i][j+1][0]*F[1],  t[i][j+1][1]*F[1],      t[i][j+1][2]],
                            [t[i+1][j+1][0]*F[1],t[i+1][j+1][1]*F[1],    t[i+1][j+1][2]],
                            [t[i+1][j][0]*F[1],  t[i+1][j][1]*F[1],      t[i+1][j][2]],
                            [t[i][j][0]*F[1],    t[i][j][1]*F[1],        t[i][j][2]]
                            ]
                            
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
        
def OLDSouthTrans(SApOls,accur):

    s = []
    Square = []
    count = 0
    ct = 0
    ApOls=SApOls
    #The I and J for part adjacent to the runway strip.
    I = range(int(1+math.ceil( max((ApOls[2][0]+(RED-SE))/ApOls[5][0],(ApOls[2][0]-((SE-NE)/2))/ApOls[5][0])/((1-ApOls[5][0])*accur))))
    J = range(int(1+math.ceil((RwyLen/2 + ApOls[3][1])/accur)))
    for i in I:
        K = []
        U = []
        T = []
        for j in J:
            par  =   j*accur - ApOls[3][1]
            par1 = (j-1)*accur - ApOls[3][1] ###incorporate these to 
            par2 = (j+1)*accur - ApOls[3][1] ###marry trans with IHS  - do with south too
            if par <= 0:
                perp =  RSW/2+(ApOls[2][0]+(RED-SE))/ApOls[5][0] - i*accur*(1-ApOls[5][0])
            elif par > 0:
                perp =  RSW/2+(ApOls[2][0]+(RED-SE))/ApOls[5][0] + (j*accur - ApOls[3][1])*((SE-NE)/RwyLen/ApOls[5][0]) - i*accur*(1-ApOls[5][0])                
            Z    =   ApOls[2][0]-i*accur*(1-ApOls[5][0])*ApOls[5][0]
            if par < RwyLen/2 and par<= 0 and par <= - SApOls[3][1] and perp<=RSW/2:
                par = - SApOls[3][1]
                perp = RSW/2
                Z = (SE-RED) 
                c = [par,perp,Z]
            if par < RwyLen/2 and par<= 0 and par <= - SApOls[3][1] and perp > RSW/2:
                par = - SApOls[3][1]
                perp = perp
                Z = Z
                c = [par,perp,Z]
            if par < RwyLen/2 and par<= 0 and par > - SApOls[3][1] and perp <= RSW/2:
                par = par
                perp = RSW/2
                Z = (SE-RED) 
                c = [par,perp,Z]
            if par < RwyLen/2 and par<= 0 and par > - SApOls[3][1] and perp > RSW/2:
                par = par
                perp = perp
                Z = Z
                c = [par,perp,Z]

            if par < RwyLen/2 and par > 0 and perp > RSW/2: 
                par = par
                perp = perp
                Z = Z
                c = [par,perp,Z]
            if par < RwyLen/2 and par > 0 and perp <= RSW/2:
                par = par
                perp = RSW/2
                Z = (SE-RED) + (j*accur -SApOls[3][1]) *(NE-SE)/RwyLen
                c = [par,perp,Z]
            if par >= RwyLen/2 and perp <= RSW/2:
                par = RwyLen/2
                perp = RSW/2
                Z = (SE-RED) + (NE-SE)/2
                c = [par,perp,Z]
            if par >= RwyLen/2 and perp > RSW/2:
                par = RwyLen/2
                perp = RSW/2+(SApOls[2][0]+(RED-SE))/SApOls[5][0] + par*((SE-NE)/RwyLen/SApOls[5][0]) - i*accur*(1-SApOls[5][0])#perp
                Z = Z
                c = [par,perp,Z]
            K.append(c)
            if perp == RSW/2:
                T.append(i)
            if par == RwyLen/2:
                U.append(j)
            sq = [c[0],c[1]]
            Square.append(sq)
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
    x = ApOls[3][0]/2+((ApOls[2][0] +(RED-SE))/ApOls[5][0]) #  = perp of Outer Edge of Trans adjacent to NthTrsld
    if (ApOls[2][0] + (RED-SE))/ApOls[3][4] <= ApOls[3][3]:
        y = ApOls[3][0]/2+(ApOls[2][0] + (RED-SE))/ApOls[3][4] * ApOls[3][2] # = perp of TranMeetApp
    elif (ApOls[2][0] + (RED-SE))/ApOls[3][4] > ApOls[3][3]:
        y = ApOls[3][0]/2+(ApOls[3][3] + \
                   (\
                    (ApOls[2][0]-(ApOls[3][2]*ApOls[3][3])) +(RED-SE)\
                    )\
                   /ApOls[3][6] )* ApOls[3][2] # = perp of TranMeetApp    
    n1 = (x-y)/((ApOls[2][0] + (RED-SE))/ApOls[3][4])
    n2 = ApOls[3][2]
    I = range(int(1+math.ceil(x/accur)))
    J = range(int(1+math.ceil(\
       (((ApOls[2][0] + (RED-SE))/ApOls[3][4]))/accur\
        )))
    D = []
    for i in I:
        K = []
        T = []
        for j in J:
            par = accur*j + ApOls[3][1]  
            perp = x - accur*n1*j - i*accur*(1-ApOls[5][0])
            Z = ApOls[2][0] - i*accur*(1-ApOls[5][0])*ApOls[5][0]
            L1 = (x-n1*j*accur) #change in perp outer line
            L2 = (ApOls[3][0]/2 + ApOls[3][2]*accur*j*(1)) # change in perp app outer line
            if par > ApOls[3][1]:
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
                    Z =  accur*j*ApOls[3][4]- (RED-SE)
                    c = [par,perp,Z]
                if perp == L1 and perp == L2:
                    par = (ApOls[2][0] + (RED-SE))/ApOls[3][4]+ ApOls[3][1]
                    perp = y
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
                if L2> L1:
                    par = (ApOls[2][0] + (RED-SE))/ApOls[3][4]+ ApOls[3][1]
                    perp = y
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
            if par <= ApOls[3][1]:
                if perp < L1 and perp > L2:
                    par = ApOls[3][1]
                    perp = perp
                    Z = Z
                    c = [par,perp,Z]
                if perp >= L1 and perp > L2 and L1>L2:
                    par = ApOls[3][1]
                    perp =L1
                    Z = ApOls[2][0]
                    c = [par,perp,Z]
                if perp < L1 and perp <= L2 and L1>L2:
                    par = ApOls[3][1]
                    perp = ApOls[3][0]/2
                    Z = (SE-RED)
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
        f.write('<SimpleData name="'+AppOLSNAME[5]+'">-</SimpleData>\n')
        for b in range(len(AppOLSDIMS[5])):
            f.write('<SimpleData name="'+AppOLSDIMS[5][b]+'">'+str(ApOls[5][b])+'</SimpleData>\n')

        				
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
            OlsSurf = 'SouthTransitional1'
        if n == 1:
            OlsSurf = 'SouthTransitional2'
        if n == 2:
            OlsSurf = 'SouthTransitional3'
        if n == 3:
            OlsSurf = 'SouthTransitional4'
        f.write( '<name>'+OlsSurf+'</name>\n') 
        hero = []
        if n == 0 or n == 1:
            I = range(int(1+math.ceil( max((ApOls[2][0]+(RED-SE))/ApOls[5][0],(ApOls[2][0]-((SE-NE)/2))/ApOls[5][0])/((1-ApOls[5][0])*accur))))
            J = range(int(1+math.ceil((RwyLen/2 + ApOls[3][1])/accur)))
        if n == 2 or n == 3:
            x = ApOls[3][0]/2+((ApOls[2][0] +(RED-SE))/ApOls[5][0]) #  = perp of Outer Edge of Trans adjacent to NthTrsld
            if (ApOls[2][0] + (RED-SE))/ApOls[3][4] <= ApOls[3][3]:
                y = ApOls[3][0]/2+(ApOls[2][0] + (RED-SE))/ApOls[3][4] * ApOls[3][2] # = perp of TranMeetApp
            elif (ApOls[2][0] + (RED-SE))/ApOls[3][4] > ApOls[3][3]:
                y = ApOls[3][0]/2+(ApOls[3][3] + \
                           (\
                            (ApOls[2][0]-(ApOls[3][2]*ApOls[3][3])) +(RED-SE)\
                            )\
                           /ApOls[3][6] )* ApOls[3][2] # = perp of TranMeetApp    
            n1 = (x-y)/((ApOls[2][0] + (RED-SE))/ApOls[3][4])
            n2 = ApOls[3][2]
            I = range(int(1+math.ceil(x/accur)))
            J = range(int(1+math.ceil(\
               (((ApOls[2][0] + (RED-SE))/ApOls[3][4]))/accur\
                )))
        
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
