import sys
import os
import math
import OLSDims
import csv
import EnvSettings

#from osgeo import osr
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

def DEM():

	Surf = 'DEM'

	fi =  open('DEM-H_09.csv','rb')
	DEMProfPlotter(fi,Surf)
	
def RwyEnds():
	E1 = NE
	E2 = SE
	ns = 'n'
	Surf = 'Runway Ends'
	rwyendplot(E1,E2,ns,Surf)
	
def NthObs(CLWY):
	E1 = NE
	E2 = SE
	ns = 'n'
	Surf = 'Northern obstacles'
	fi =  open('ObsData.csv','rb')
	Obs(E1,E2,ns,Surf,fi,CLWY)
def SthObs(CLWY):
	E1 = SE
	E2 = NE
	ns = 's'
	fi =  open('ObsData.csv','rb')
	Obs(E1,E2,ns,Surf,fi,CLWY)

def NthObs2(CLWY,ToOls):
	E1 = NE
	E2 = SE
	ns = 'n'
	offset = 3000
	fi =  open('ObsProfData.csv','rb')
	Surf = 'Northern obstacles'
	Obs2(E1,E2,ns,Surf,fi,CLWY,ToOls,offset)
def SthObs2(CLWY,ToOls):
	E1 = SE
	E2 = NE
	ns = 's'
	Surf = 'Southern obstacles'
	fi =  open('ObsProfData.csv','rb')
	Obs2(E1,E2,ns,Surf,fi,CLWY,ToOls)

          
def DEMProfPlotter(fi,Surf):
	f.write( '<Folder><name>'+Surf+'</name><open>1</open>\n')
	next(fi)
	for row in csv.reader(fi):
            
##		if float(row[1]) > 0 and row[0] == ns and float(row[4])/float(row[1]) > ToOls[5][0]:
            if  len(row[0]) > 0:
                f.write(   "<Placemark>\n")
                f.write( '<name>'+str(round(float(row[0].strip()),1))+'</name>\n')
                f.write("""        
                <styleUrl>#m_ylw-pushpin</styleUrl>
        
                <Point>
        
                <extrude>1</extrude>

                <altitudeMode>absolute</altitudeMode>

                <gx:drawOrder>1</gx:drawOrder> 
                <coordinates>""")

                f.write(str(row[1])+","+str(row[2])+","+str(row[0]))
                f.write(   "\n")
                f.write(   "</coordinates></Point>")
                f.write('</Placemark>\n')
	f.write("</Folder>")
	
	
def rwyendplot(E1,E2,ns,Surf):
	f.write( '<Folder><name>'+Surf+'</name><open>1</open>\n')
	E = [[E2,E1],[E1,E2]]
	T = [
            [NTE,NTN,STE,STN],
            [STE,STN,NTE,NTN],
            ]
	for i in range(2):
            f.write(   "<Placemark>\n")
            
            f.write( '<name>Runway Ends</name>\n')
            f.write("""        
            <styleUrl>#m_ylw-pushpin</styleUrl>
    
            <Point>
    
            <extrude>1</extrude>

            <altitudeMode>absolute</altitudeMode>

            <gx:drawOrder>1</gx:drawOrder> 
            <coordinates>""")
            Utm = mdl.toUTM(T[i][0],T[i][1],T[i][2],T[i][3],ARP,E[i][0],E[i][1],0,0,0,ns)
            Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, E1))
            f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
            f.write(   "\n")
            f.write(   "</coordinates></Point>")
            f.write('</Placemark>\n')
        f.write("</Folder>")
            
def Obs2(E1,E2,ns,Surf,fi,CLWY,ToOls,offset):
	f.write( '<Folder><name>'+Surf+'</name><open>1</open>\n')
	
	for row in csv.reader(fi):
		f.write(   "<Placemark>\n")
		if float(row[1]) > 0 and row[0] == ns and float(row[4])/float(row[1]) > ToOls[5][0]:
			
			f.write( '<name>'+row[1]+','+row[4]+'</name>\n')
			f.write("""        
			<styleUrl>#m_ylw-pushpin</styleUrl>
		
			<Point>
		
			<extrude>1</extrude>

			<altitudeMode>absolute</altitudeMode>

			<gx:drawOrder>1</gx:drawOrder> 
			<coordinates>""")
			Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,E2,E1,(float(row[1])+CLWY)*(-1),float(row[4])*(1)*10 + offset,0,ns)
			Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, float(row[4])))
			f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
			f.write(   "\n")
			f.write(   "</coordinates></Point>")
		f.write('</Placemark>\n')
	f.write("</Folder>")
	
	
def Obs(E1,E2,ns,Surf,fi,CLWY):
	f.write( '<Folder><name>'+Surf+'</name><open>1</open>\n')
	for row in csv.reader(fi):
		f.write(   "<Placemark>\n")
		if row[2] == ns:
			
			f.write( '<name>'+row[0]+' '+row[1]+' '+row[4]+' m AHD'+'</name>\n')
			f.write("""        
			<styleUrl>#m_ylw-pushpin</styleUrl>
		
			<Point>
		
			<extrude>1</extrude>

			<altitudeMode>absolute</altitudeMode>

			<gx:drawOrder>1</gx:drawOrder> 
			<coordinates>""")
			Utm = mdl.toUTM(NTE,NTN,STE,STN,ARP,E2,E1,(float(row[5])+CLWY)*(-1),float(row[6])*(-1),float(row[4]),ns)
			Wgs = list(mdl.U_W(Utm[0],Utm[1],zone, float(row[4])))
			f.write(str(Wgs[0])+","+str(Wgs[1])+","+str(Wgs[2]))
			f.write(   "\n")
			f.write(   "</coordinates></Point>")
		f.write('</Placemark>\n')
	f.write("</Folder>")
