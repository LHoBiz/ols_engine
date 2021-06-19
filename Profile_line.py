# -*- coding: cp1252 -*-
import sys
import os
import math
import OLSDims
import csv
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

def NthProf(NCLWY,accur,ToOls):
	E1=NE
	E2=SE
	CLWY = NCLWY
	ns = 'n'
	Surf = 'NorthProfile'
	fi =  open('ProfileData.csv','rb')
	offset = 3000
	Profile(E1,E2,CLWY,ns,Surf,fi,offset)
##	Slope(E1,E2,CLWY,ns,"Slope",accur,ToOls,offset)
##	fi =  open('ObsProfData.csv','rb')
	#Obst(E1,E2,CLWY,ns,"Obstacles",accur,ToOls,fi,offset)

def Profile(E1,E2,CLWY,ns,Surf,fi,offset):
    

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
    f.write('<SimpleData name="'+Surf+'">-</SimpleData>\n')
    f.write('</SchemaData>\n')
    f.write('</ExtendedData>\n')
    f.write('</ScreenOverlay>\n')
    f.write( '<name>'+Surf+'</name>\n')
    f.write(   """<Placemark>
    <name>Untitled Path</name>                        
    <styleUrl>#msn_ylw-pushpin</styleUrl>                        
    <LineString>                                
    <tessellate>1</tessellate>                                
    <coordinates>""")
    Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,E2,E1,0,0,0,ns)
    Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, 0))
    f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
    f.write(   "\n")
    Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,E2,E1,0,offset + E1*10,0,ns)
    Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, 0))
    f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
    f.write(   "\n")
    for row in csv.reader(fi):
        if float(row[3]) > 0:
            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,E2,E1,float(row[0])*(-1) - CLWY,float(row[3])*10 + offset,0,ns)
            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, 0))
            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
            f.write(   "\n")
    f.write(   """</coordinates></LineString></Placemark>""")
    f.write( '\n')
    f.write( '\n')
    f.write( '</Folder>\n')

		
def Slope(E1,E2,CLWY,ns,Surf,accur,ToOls,offset):
	
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
    f.write('<SimpleData name="'+Surf+'">-</SimpleData>\n')
    f.write('</SchemaData>\n')
    f.write('</ExtendedData>\n')
    f.write('</ScreenOverlay>\n')
    f.write( '<name>'+Surf+'</name>\n')
    f.write(   """<Placemark>
    <name>Untitled Path</name>                        
    <styleUrl>#msn_ylw-pushpin</styleUrl>                        
    <LineString>                                
    <tessellate>1</tessellate>                                
    <coordinates>""")
    
    for i in range(int(float(ToOls[4][0])/accur)+1):
            Par = i*accur
            
            if Par >= float(ToOls[4][0]):
                    Par = float(ToOls[4][0])
            Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,E2,E1,Par*(-1) - CLWY,(i*accur*ToOls[5][0] + E1)*10 + offset ,0,ns)
            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, 0))
            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
            f.write(   "\n")
    f.write(   """</coordinates></LineString></Placemark>""")
    
    f.write( '\n')
    f.write( '\n')
    f.write( '</Folder>\n')
		
def Obst(E1,E2,CLWY,ns,Surf,accur,ToOls,fi,offset):

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
    f.write('<SimpleData name="'+Surf+'">-</SimpleData>\n')
    f.write('</SchemaData>\n')
    f.write('</ExtendedData>\n')
    f.write('</ScreenOverlay>\n')
    f.write( '<name>'+Surf+'</name>\n')
    f.write(   """<Placemark>
    <name>Untitled Path</name>                        
    <styleUrl>#msn_ylw-pushpin</styleUrl>                        
    <LineString>                                
    <tessellate>1</tessellate>                                
    <coordinates>""")
    for row in csv.reader(fi):
        if float(row[0]) > 0:
            if float(row[3])/float(row[0]) >= ToOls[5][0]:
                    
                Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,E2,E1,float(row[0])*(-1) - CLWY,float(row[3])*10 + offset,0,ns)
                Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, 0))
                f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
                f.write(   "\n")
    f.write(   """</coordinates></LineString></Placemark>""")
    f.write( '\n')
    f.write( '\n')
    f.write( '</Folder>\n')

		
