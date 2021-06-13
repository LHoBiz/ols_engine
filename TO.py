# -*- coding: cp1252 -*-
import math
import OLSDims
import EnvSettings

from osgeo import osr
import mdl
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
CN = ip.CN
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
##STOInEdge=ip.STOInEdge
##NTOInEdge=ip.NTOInEdge


RwyLen = math.sqrt((NTE-STE)*(NTE-STE) + (NTN-STN)*(NTN-STN))
NCLWY=ip.NCLWY
SCLWY=ip.SCLWY


def NorthTO(NToOls,accur):
    ToOls=NToOls
    Div = ToOls[2][0]
    Slope = ToOls[5][0]
    s = []
    Square = []
    Elev = NE
    ToOls=NToOls
    TOTurn15d=NTOTurn15d
    TOAlt = NTOAlt
    TOL = ToOls[4][0]
    MTOW22700kg = NMTOW22700kg
    Ins=NIns
    
    ToOls[1][0] = NCLWY
    
    
    if MTOW22700kg == 'N' and TOAlt == 'N':
        innEdge = mdl.F_M(150,1)
    if MTOW22700kg == 'Y' and TOAlt == 'N':
        innEdge = mdl.F_M(250,1)

    if TOAlt == 'N':
        if TOTurn15d == 'N':
            if TOL*Slope + innEdge/2 < mdl.F_M(1000,1):
                outEdge = TOL*Slope + innEdge/2
            elif TOL*Slope + innEdge/2 >= mdl.F_M(1000,1):
                outEdge = mdl.F_M(1000,1)
        if TOTurn15d == 'Y':
            print 'Stop - another method is required to determine take-off area'
    if TOAlt == 'Y':
        if Ins == 'Y' or  TOTurn15d == 'Y': 
            outEdge = mdl.F_M(900,1) 
        else:
            outEdge = mdl.F_M(600,1)
	innEdge = mdl.F_M(90,1)
    innEdge = ToOls[0][0]
    outEdge = ToOls[3][0]
    J = range(1+int(math.ceil(TOL/mdl.iN(accur))))
    I = range(1+int(math.ceil((outEdge/2)/mdl.iS(accur))))
    for i in I:
        K = []
        T = []
        for j in J:
            D1 = ((outEdge-innEdge)/2)/Div + ToOls[1][0]
            D10 = D1 - accur
            D11 = D1 + accur
            D = (TOL+ToOls[1][0]) - j*accur
            Dm1= (TOL+ToOls[1][0]) - (j-1)*accur
            Dp1= (TOL+ToOls[1][0]) - (j+1)*accur
            H = Slope * (D-ToOls[1][0]) + NE
            L = (innEdge/2)+(Div*(D-ToOls[1][0])) - i*accur
            L1 = (innEdge/2)+(Div*(D1-ToOls[1][0])) - i*accur
            H1 = Slope * (D1-ToOls[1][0]) + NE
            
            if L > 0 and outEdge/2 - i*accur > 0:
                ## area 1
                if D > D11:
                    if L >= outEdge/2 - i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D,L,H])

                ## area 2  
                if D <= D11 and D > D1:
                    if L >= outEdge/2- i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D,L,H])
                    K.append([D1,L1,H1])
                    
                ## area 3  
                if D <= D1 and D > D10:
                    if L >= outEdge/2- i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D1,L1,H1])
                    K.append([D,L,H])

                ## area 4  
                if D <= D10 and D > ToOls[1][0]:
                    if L >= outEdge/2- i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D,L,H])

                ## area 5  
                if D <= ToOls[1][0]:
                    if L >= outEdge/2- i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D,L,H])
                    K.append([ToOls[1][0],innEdge/2,Elev])

                    
            if L <= 0 or outEdge/2 - i*accur <= 0:
                L = 0
                L1 = 0
                if D > D11:
                    K.append([D,L,H])

                ## area 2  
                if D <= D11 and D > D1:
                    K.append([D,L,H])
                    K.append([D1,L1,H1])
                    
                ## area 3  
                if D <= D1 and D > D10:
                    K.append([D1,L1,H1])
                    K.append([D,L,H])

                ## area 4  
                if D <= D10 and D > ToOls[1][0]:
                    K.append([D,L,H])

                ## area 5  
                if D <= ToOls[1][0]:
                    K.append([D,L,H])
                    K.append([ToOls[1][0],innEdge/2,Elev])

            if L == 0:
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
        f.write('<SimpleData name="'+TOOLSNAME[0][0]+'">-</SimpleData>\n')
        for b in range(len(TOOLSNAME[1])):
            f.write('<SimpleData name="'+TOOLSNAME[1][b][0]+'">'+str(ToOls[b][0])+'</SimpleData>\n')

        				
        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')

        if n == 0:
            f.write( '<name>North'+TOOLSNAME[0][0]+'1</name>\n')
            
               
        if n == 1:
            f.write( '<name>North'+TOOLSNAME[0][0]+'2</name>\n')
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
                        f.write(   '<SimpleData name="Surface">'+TOOLSNAME[0][0]+'</SimpleData>')
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

def SouthTO(SToOls,accur):
    ToOls=SToOls
    Div = ToOls[2][0]
    Slope = ToOls[5][0]
    s = []
    Square = []
    Elev = SE
    ToOls=SToOls
    TOTurn15d=STOTurn15d
    TOAlt = STOAlt
    TOL = ToOls[4][0]
    MTOW22700kg = SMTOW22700kg
    Ins=SIns
    ToOls[1][0] =SCLWY 
    
    if MTOW22700kg == 'N' and TOAlt == 'N':
        innEdge = mdl.F_M(150,1)
    if MTOW22700kg == 'Y' and TOAlt == 'N':
        innEdge = mdl.F_M(250,1)

    if TOAlt == 'N':
        if TOTurn15d == 'N':
            if TOL*Slope + innEdge/2 < mdl.F_M(1000,1):
                outEdge = TOL*Slope + innEdge/2
            elif TOL*Slope + innEdge/2 >= mdl.F_M(1000,1):
                outEdge = mdl.F_M(1000,1)
        if TOTurn15d == 'Y':
            print 'Stop - another method is required to determine take-off area'
    if TOAlt == 'Y':
        if Ins == 'Y' or  TOTurn15d == 'Y': 
            outEdge = mdl.F_M(900,1) 
        else:
            outEdge = mdl.F_M(600,1)
	innEdge = mdl.F_M(90,1)
    innEdge = ToOls[0][0]
    outEdge = ToOls[3][0]
    J = range(1+int(math.ceil(TOL/mdl.iN(accur))))
    I = range(1+int(math.ceil((outEdge/2)/mdl.iS(accur))))
    for i in I:
        K = []
        T = []
        for j in J:
            D1 = ((outEdge-innEdge)/2)/Div + ToOls[1][0]
            D10 = D1 - accur
            D11 = D1 + accur
            D = (TOL+ToOls[1][0]) - j*accur
            Dm1= (TOL+ToOls[1][0]) - (j-1)*accur
            Dp1= (TOL+ToOls[1][0]) - (j+1)*accur
            H = Slope * (D-ToOls[1][0]) + Elev
            L = (innEdge/2)+(Div*(D-ToOls[1][0])) - i*accur
            L1 = (innEdge/2)+(Div*(D1-ToOls[1][0])) - i*accur
            H1 = Slope * (D1-ToOls[1][0]) + Elev
            
            if L > 0 and outEdge/2 - i*accur > 0:
                ## area 1
                if D > D11:
                    if L >= outEdge/2 - i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D,L,H])

                ## area 2  
                if D <= D11 and D > D1:
                    if L >= outEdge/2- i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D,L,H])
                    K.append([D1,L1,H1])
                    
                ## area 3  
                if D <= D1 and D > D10:
                    if L >= outEdge/2- i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D1,L1,H1])
                    K.append([D,L,H])

                ## area 4  
                if D <= D10 and D > ToOls[1][0]:
                    if L >= outEdge/2- i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D,L,H])

                ## area 5  
                if D <= ToOls[1][0]:
                    if L >= outEdge/2- i*accur: 
                        L = outEdge/2 - i*accur
                    K.append([D,L,H])
                    K.append([ToOls[1][0],innEdge/2,Elev])

                    
            if L <= 0 or outEdge/2 - i*accur <= 0:
                L = 0
                L1 = 0
                if D > D11:
                    K.append([D,L,H])

                ## area 2  
                if D <= D11 and D > D1:
                    K.append([D,L,H])
                    K.append([D1,L1,H1])
                    
                ## area 3  
                if D <= D1 and D > D10:
                    K.append([D1,L1,H1])
                    K.append([D,L,H])

                ## area 4  
                if D <= D10 and D > ToOls[1][0]:
                    K.append([D,L,H])

                ## area 5  
                if D <= ToOls[1][0]:
                    K.append([D,L,H])
                    K.append([ToOls[1][0],innEdge/2,Elev])

            if L == 0:
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
        f.write('<SimpleData name="'+TOOLSNAME[0][0]+'">-</SimpleData>\n')
        for b in range(len(TOOLSNAME[1])):
            f.write('<SimpleData name="'+TOOLSNAME[1][b][0]+'">'+str(ToOls[b][0])+'</SimpleData>\n')

        				
        f.write('</SchemaData>\n')
        f.write('</ExtendedData>\n')
        f.write('</ScreenOverlay>\n')

        if n == 0:
            f.write( '<name>South'+TOOLSNAME[0][0]+'1</name>\n')
            
               
        if n == 1:
            f.write( '<name>South'+TOOLSNAME[0][0]+'2</name>\n')
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
                        f.write(   '<SimpleData name="Surface">'+TOOLSNAME[0][0]+'</SimpleData>')
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
