import sys
import os
import math
import csv
import OLSDims
import EnvSettings

from osgeo import osr
import mdl
ip = mdl.Data()
f=ip.f
NTOL=ip.NTOL
STOL=ip.STOL
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
NCLWY=ip.NCLWY
SCLWY=ip.SCLWY

def NorthObsCheck(ToOLS,ApOls):
	E1=NE
	E2=SE
	CLWY = NCLWY
	TOL = ToOLS[4][0]
	ns = 'n'
	Surf = 'NorthObs_Check'
	fi =  open('ObsData.csv','rb')
	report = Obs_Check(E1,E2,TOL,ns,Surf,ToOLS,ApOls,fi,CLWY)
        return report
def SouthObsCheck(ToOLS,ApOls):
	E1=SE
	E2=NE
	CLWY = SCLWY
	TOL = ToOLS[4][0]
	ns = 's'
	Surf = 'SouthObs_Check'
	fi =  open('ObsData.csv','rb')
	report = Obs_Check(E1,E2,TOL,ns,Surf,ToOLS,ApOls,fi,CLWY)
	return report
	

def Obs_Check(E1,E2,TOL,ns,Surf,ToOls,ApOls,fi,CLWY):
    report = []
    report.append(str(ns)+'thern clearway length = '+str(CLWY))
    report.append(str(ns)+'thern inner edge elevation = '+str(E1))
    for row in csv.reader(fi):
		ObsPar =float(row[5])
		ObsPerp=float(row[6])
		ObsZ   =float(row[4])
		
		#Check Take-off surface
		
		innEdge = ToOls[0][0]
		outEdge = ToOls[3][0]
		if ObsPar <= TOL and ObsPar >= 0 and row[2] == ns:
			if (ObsPar) < (ToOls[3][0]/ToOls[2][0]/2):
				TOPerp = (ObsPar*ToOls[2][0]) + (ToOls[0][0]/2)
			elif (ObsPar) >= (ToOls[3][0]/ToOls[2][0]/2):
				TOPerp = outEdge/2
			TOZ = ObsPar*ToOls[5][0] + E1
			if abs(ObsPerp) <= TOPerp and ObsZ > TOZ:
				Encr = [row[2],row[0],row[1]]
				report.append(Encr)
				Encr = ['Dist from CLWY = '+str(ObsPar),'Dist from Extended CtrLine = '+str(ObsPerp),'Obst height (m AHD) = '+str(ObsZ)]
				report.append(Encr)
				Encr = ['Penetrates Take-off Surface by',str(ObsZ-TOZ) + " m"]
				report.append(Encr)
		
		#Check Approach Surface
		
		innEdge = ApOls[3][0]
		outEdge = ApOls[3][2]*ApOls[3][8]*2 + ApOls[3][0]

		if ObsPar <= ApOls[3][8] and ObsPar >= 0 and row[2] == ns:
			ApPerp = (ObsPar*ApOls[3][2]) + (ApOls[3][0]/2)
			
			if ObsPar <= ApOls[3][3]:
				ApZ = ObsPar*ApOls[3][4] + E1
				
			if ObsPar > ApOls[3][3] and ObsPar <= (ApOls[3][3]+ApOls[3][5]):
				ApZ = ApOls[3][3]*ApOls[3][4]+ ObsPar*ApOls[3][6] + E1
				
			if ObsPar > (ApOls[3][3]+ApOls[3][5]) and ObsPar <= (ApOls[3][3]+ApOls[3][5]+ApOls[3][7]):
				ApZ = ApOls[3][3]*ApOls[3][4]+ ApOls[3][5]*ApOls[3][6] + E1
				
			if abs(ObsPerp) <= ApPerp and ObsZ > ApZ:
				Encr = [row[2],row[0],row[1]]
				report.append(Encr)
				Encr = ['Dist from CLWY = '+str(ObsPar),'Dist from Extended CtrLine = '+str(ObsPerp),'Obst height (m AHD) = '+str(ObsZ)]
				report.append(Encr)
				Encr = ['Penetrates Approach Surface by',str(ObsZ-ApZ) + " m"]
				report.append(Encr)

    return report
		#Check Transitional Surface
		
		# innEdge = ApOls[3][0]
		# outEdge = ApOls[3][2]*ApOls[3][8]*2 + ApOls[3][0]

		# if ObsPar <= ApOls[3][8] and ObsPar >= 0:
			# ApPerp = (ObsPar*ApOls[3][2]) + (ApOls[3][0]/2)
			
			# if ObsPar <= ApOls[3][3]:
				# ApZ = ObsPar*ApOls[3][4] + E1
				
			# if ObsPar > ApOls[3][3] and ObsPar <= (ApOls[3][3]+ApOls[3][5]):
				# ApZ = ApOls[3][3]*ApOls[3][4]+ ObsPar*ApOls[3][6] + E1
				
			# if ObsPar > (ApOls[3][3]+ApOls[3][5]) and ObsPar <= (ApOls[3][3]+ApOls[3][5]+ApOls[3][7]):
				# ApZ = ApOls[3][3]*ApOls[3][4]+ ApOls[3][5]*ApOls[3][6] + E1
				
			# if abs(ObsPerp) <= ApPerp and ObsZ > ApZ:
				# print row[2],row[0],row[1],'Penetrates Approach Surface by',ObsZ-ApZ
				
				
				
				
				
				
				
				
				
				
				
				
				