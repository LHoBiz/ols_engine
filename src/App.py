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

def NorthApp(ApOls,accur):
    E1 = NE
    E2 = SE
    ns = 'n'
    Surf = 'NorthApproach'
    Approach(E1,E2,ns,Surf,accur,ApOls)
def SouthApp(ApOls,accur):
    E1 = SE
    E2 = NE
    ns = 's'
    Surf = 'SouthApproach'
    Approach(E1,E2,ns,Surf,accur,ApOls)


def Approach(E1,E2,ns,Surf,accur,ApOls):
    s = []
    Square = []
    #I = range(int(math.ceil(150/mdl.iN(accur))+1))
    J = range(int(ApOls[3][8]/mdl.iN(accur)+1))
    I = range(int(math.ceil((ApOls[3][0]/2 + ApOls[3][2]*ApOls[3][8])/mdl.iN(accur))+1))
    count = 0
    ct = 0
    for l in I:
        T = []
        K = []  
        for j in J:
            a = ApOls[3][0]/2 + ApOls[3][2]*ApOls[3][8] - l*mdl.iN(accur) - \
                     ApOls[3][2]*mdl.iN(accur)*j
            
            b = ApOls[3][1] + ApOls[3][8] - mdl.iN(accur)*j
            bUp = ApOls[3][1] + ApOls[3][8] - mdl.iN(accur)*(j+1)
            b1= ApOls[3][1]+ApOls[3][3]
            b2= ApOls[3][1]+ApOls[3][3]+ApOls[3][5]
            b3= ApOls[3][1]+ApOls[3][3]+ApOls[3][5] +ApOls[3][7]



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

            ###fix this up
##            b4= ApOls[3][1]+(ApOls[2][0] + (RED-E1))/ApOls[3][4]
            if a > 0:
                    
                if b <= b3 and b > b2+mdl.iN(accur) and b2 != b3:
                    e = E1 + ApOls[3][3]*ApOls[3][4] +\
                             ApOls[3][5]*ApOls[3][6]
                    c = [b,a,e]
                    K.append(c)

                elif b <= b2+mdl.iN(accur) and b > b2:
                    e = E1 + ApOls[3][3]*ApOls[3][4] +\
                             ApOls[3][5]*ApOls[3][6]
                             
                    e1 = E1 + ApOls[3][3]*ApOls[3][4] + \
                              ApOls[3][5]*ApOls[3][6]
                    B1 = b2
                    A1 = ApOls[3][0]/2 + ApOls[3][2]*(B1-ApOls[3][1]) - l*mdl.iN(accur)
                    c = [b,a,e]
                    K.append(c)
                    c = [B1,A1,e1]
                    K.append(c)
                elif b == b2:
                    e = E1 + ApOls[3][3]*ApOls[3][4] + ApOls[3][5]*ApOls[3][6]
                    c = [b,a,e]
                    K.append(c)
                elif b >= b2-mdl.iN(accur) and b < b2 and b3!=b2:
                    e = E1 + ApOls[3][3]*ApOls[3][4] + (b-b1)*ApOls[3][6]
                    e1 = E1 + ApOls[3][3]*ApOls[3][4] + ApOls[3][5]*ApOls[3][6]
                    B1 = b2
                    A1 = ApOls[3][0]/2 + ApOls[3][2]*(B1-ApOls[3][1]) - l*mdl.iN(accur)
                    c = [B1,A1,e1]
                    K.append(c)
                    c = [b,a,e]
                    K.append(c)
                elif b >= b2-mdl.iN(accur) and b < b2 and b3==b2:
                    e = E1 + ApOls[3][3]*ApOls[3][4] + (b-b1)*ApOls[3][6]
                    c = [b,a,e]
                    K.append(c)

                elif b < b2-mdl.iN(accur) and b > b1+mdl.iN(accur):
                    e = E1 + ApOls[3][3]*ApOls[3][4] + (b-b1)*ApOls[3][6]
                    c = [b,a,e]
                    K.append(c)

                elif b <= b1+mdl.iN(accur) and b > b1:
                    e = E1 + ApOls[3][3]*ApOls[3][4]+(b-b1)*ApOls[3][6]
                    e1 = E1 + ApOls[3][3]*ApOls[3][4]
                    B1 = b1
                    A1 = ApOls[3][0]/2 + ApOls[3][2]*(B1-ApOls[3][1]) - l*mdl.iN(accur)
                    c = [b,a,e]
                    K.append(c)
                    c = [B1,A1,e1]
                    K.append(c)

                elif b == b1:
                    e = E1 + ApOls[3][3]*ApOls[3][4]
                    c = [b,a,e]
                    K.append(c)
                    
                elif b >= b1-mdl.iN(accur) and b < b1:
                    e = E1 +(b-ApOls[3][1])*ApOls[3][4]
                    e1 = E1 + ApOls[3][3]*ApOls[3][4]
                    B1 = b1
                    A1 = ApOls[3][0]/2 + ApOls[3][2]*(B1-ApOls[3][1]) - l*mdl.iN(accur)
                    c = [B1,A1,e1]
                    K.append(c)
                    c = [b,a,e]
                    K.append(c)

                elif b < b1-mdl.iN(accur):
                    e = E1 +(b-ApOls[3][1])*ApOls[3][4]
                    c = [b,a,e]
                    K.append(c)
            elif a <= 0:
                if b <= b3 and b > b2+mdl.iN(accur) and b2 != b3:
                    e = E1 + ApOls[3][3]*ApOls[3][4] +\
                             ApOls[3][5]*ApOls[3][6]
                    c = [b,0,e]
                    K.append(c)

                elif b <= b2+mdl.iN(accur) and b > b2:
                    e = E1 + ApOls[3][3]*ApOls[3][4] +\
                             ApOls[3][5]*ApOls[3][6]
                             
                    e1 = E1 + ApOls[3][3]*ApOls[3][4] + \
                              ApOls[3][5]*ApOls[3][6]
                    B1 = b2
                    A1 = ApOls[3][0]/2 + ApOls[3][2]*(B1-ApOls[3][1]) - l*mdl.iN(accur)
                    c = [b,0,e]
                    K.append(c)
                    c = [B1,0,e1]
                    K.append(c)
                elif b == b2:
                    e = E1 + ApOls[3][3]*ApOls[3][4] + ApOls[3][5]*ApOls[3][6]
                    c = [b,0,e]
                    K.append(c)
                elif b >= b2-mdl.iN(accur) and b < b2 and b3!=b2:
                    e = E1 + ApOls[3][3]*ApOls[3][4] + (b-b1)*ApOls[3][6]
                    e1 = E1 + ApOls[3][3]*ApOls[3][4] + ApOls[3][5]*ApOls[3][6]
                    B1 = b2
                    A1 = ApOls[3][0]/2 + ApOls[3][2]*(B1-ApOls[3][1]) - l*mdl.iN(accur)
                    c = [B1,0,e1]
                    K.append(c)
                    c = [b,0,e]
                    K.append(c)
                elif b >= b2-mdl.iN(accur) and b < b2 and b3==b2:
                    e = E1 + ApOls[3][3]*ApOls[3][4] + (b-b1)*ApOls[3][6]
                    c = [b,0,e]
                    K.append(c)

                elif b < b2-mdl.iN(accur) and b > b1+mdl.iN(accur):
                    e = E1 + ApOls[3][3]*ApOls[3][4] + (b-b1)*ApOls[3][6]
                    c = [b,0,e]
                    K.append(c)

                elif b <= b1+mdl.iN(accur) and b > b1:
                    e = E1 + ApOls[3][3]*ApOls[3][4]+(b-b1)*ApOls[3][6]
                    e1 = E1 + ApOls[3][3]*ApOls[3][4]
                    B1 = b1
                    A1 = ApOls[3][0]/2 + ApOls[3][2]*(B1-ApOls[3][1]) - l*mdl.iN(accur)
                    c = [b,0,e]
                    K.append(c)
                    c = [B1,0,e1]
                    K.append(c)

                elif b == b1:
                    e = E1 + ApOls[3][3]*ApOls[3][4]
                    c = [b,0,e]
                    K.append(c)
                    
                elif b >= b1-mdl.iN(accur) and b < b1:
                    e = E1 +(b-ApOls[3][1])*ApOls[3][4]
                    e1 = E1 + ApOls[3][3]*ApOls[3][4]
                    B1 = b1
                    A1 = ApOls[3][0]/2 + ApOls[3][2]*(B1-ApOls[3][1]) - l*mdl.iN(accur)
                    c = [B1,0,e1]
                    K.append(c)
                    c = [b,0,e]
                    K.append(c)
                    

                elif b < b1-mdl.iN(accur):
                    e = E1 +(b-ApOls[3][1])*ApOls[3][4]
                    c = [b,0,e]
                    K.append(c)
                   
                
            if a == 0:
                T.append(j)

            sq = [c[0],c[1]]
            Square.append(sq)

        s.append(K)
       
        if len(T) > 0:
            J = range(T[0]+1)

    F = [1,-1]
    
    for n in range(2):
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
        f.write('<SimpleData name="'+AppOLSNAME[3]+'">-</SimpleData>\n')
        for b in range(len(AppOLSDIMS[3])):
            f.write('<SimpleData name="'+AppOLSDIMS[3][b]+'">'+str(ApOls[3][b])+'</SimpleData>\n')
        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')
        OlsSurf = Surf
        f.write( '<name>'+OlsSurf+'</name>\n')
        hero = []
        I = range(len(s))
        for i in I:
            for j in range(len(s[i])):
                if i < max(I):
                    if j < (len(s[i+1])-1):
                        if n == 0:
                            xx =[
                            [s[i][j][0]*F[1],    s[i][j][1]*F[0],        s[i][j][2]],
                            [s[i][j+1][0]*F[1],  s[i][j+1][1]*F[0],      s[i][j+1][2]],
                            [s[i+1][j+1][0]*F[1],s[i+1][j+1][1]*F[0],    s[i+1][j+1][2]],
                            [s[i+1][j][0]*F[1],  s[i+1][j][1]*F[0],      s[i+1][j][2]],
                            [s[i][j][0]*F[1],    s[i][j][1]*F[0],        s[i][j][2]]
                            ]
                        if n == 1:
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
                            e = xx[h][2]
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
        f.write( '</Folder>\n')
