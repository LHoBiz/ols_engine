# -*- coding: cp1252 -*-
import WelcomeNote
import math
import OLSDims
import mdl
import EnvSettings
import os
from osgeo import osr

import App
import InApp
import Trans
import InTrans
import Baulked
import IHS
import TO
import Circ
import CAAP92App
import CAAP92Trans
import Conl
import OHS
import ObsData
class dataInput:
    ip = mdl.Data()
    f=ip.f
    AppOLS = OLSDims.AppDim.AppOLS
    ToOLS = OLSDims.TODim.ToOLS
    AppOLSNAME=OLSDims.AppDim.AppOLSNAME
    AppOLSDIMS=OLSDims.AppDim.AppOLSDIMS
    TOOLSNAME=OLSDims.TODim.TOOLSNAME
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
    NMTOW22700kg=ip.NMTOW22700kg
    SMTOW22700kg=ip.SMTOW22700kg
    NTOTurn15d=ip.NTOTurn15d
    STOTurn15d=ip.STOTurn15d
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
    ToSurfs = range(len(ToOLS[0]))
    NE=ip.NE
    SE=ip.SE
    NTE=ip.NTE
    NTN=ip.NTN
    STE=ip.STE
    STN=ip.STN
    ARP=ip.ARP
    ARPE=ip.ARPE
    ARPN=ip.ARPN
    ARPCoords=[ARPE,ARPN,ARP]
    SE=ip.SE
    NE=ip.NE
    zone=ip.zone
    KML_NAME=ip.KML_NAME
    completeName=ip.completeName
    NCLWY=ip.NCLWY
    SCLWY=ip.SCLWY
    NTOIns=ip.NTOIns
    STOIns=ip.STOIns


    RwyLen = math.sqrt((NTE-STE)*(NTE-STE) + (NTN-STN)*(NTN-STN))

    #####################################################
    ## Set OLS logic based on the rules set out in docs #
    #####################################################
    
    if CN == 'ALA':
        NApOls = []
        SApOls = []
    else:
            
        if NTOIns == 'N':
            if CN == 2:
                NToOls = []
                for i in ToSurfs:
                    NToOls.append(ToOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            NToOls = []
                            for i in ToSurfs:
                                NToOls.append(ToOLS[1][i])                            
                else:
                    NToOls = []
                    for i in ToSurfs:
                        NToOls.append(ToOLS[0][i])
            if CN == 3 or CN == 4:
                NToOls = []
                for i in ToSurfs:
                    NToOls.append(ToOLS[2][i])
                if NMTOW22700kg == 'N' and DayOnly == 'Y':
                    NToOls[0] = 90
                if NTOTurn15d == 'N' and DayOnly == 'Y':
                    NToOls[3] = 1200
        if NTOIns == 'Y':
            if CN == 2:
                NToOls = []
                for i in ToSurfs:
                    NToOls.append(ToOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            NToOls = []
                            for i in ToSurfs:
                                NToOls.append(ToOLS[1][i])                            
                else:
                    NToOls = []
                    for i in ToSurfs:
                        NToOls.append(ToOLS[0][i])
            if CN == 3 or CN == 4:
                NToOls = []
                for i in ToSurfs:
                    NToOls.append(ToOLS[2][i])                
        if NIns == 'N':
            if CN == 2:
                
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            NApOls = []
                            for i in Surfaces:
                                NApOls.append(AppOLS[1][i])                      
                else:
                    NApOls = []
                    NToOls = []
                    for i in Surfaces:
                        NApOls.append(AppOLS[0][i])
                    for i in ToSurfs:
                        NToOls.append(ToOLS[0][i])
            if CN == 3:
                NApOls = []
                NToOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[2][i])
                for i in ToSurfs:
                    NToOls.append(ToOLS[2][i])
                if RWY_WID <= 30:
                    NApOls[3][0] = 90
                if NMTOW22700kg == 'N' and DayOnly == 'Y':
                    NToOls[0] = 90
                if NTOTurn15d == 'N' and DayOnly == 'Y':
                    NToOls[3] = 1200
            if CN == 4:
                NApOls = []
                NToOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[3][i])
                for i in ToSurfs:
                    NToOls.append(ToOLS[2][i])
                if NMTOW22700kg == 'N' and DayOnly == 'Y':
                    NToOls[0] = 90
                if NTOTurn15d == 'N' and DayOnly == 'Y':
                    NToOls[3] = 1200
        if NIns == 'Y' and NPrc == 'N':
            if CN == 1 or CN == 2:
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[4][i])            
            if CN == 3:
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[5][i])
            if CN == 4:
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[6][i])       
        if NIns == 'Y' and NPrc == 'Y1':
            if CN == 1 or CN == 2:
                NApOls = []
                for i in Surfaces:
                    NApOls.append(AppOLS[7][i])
                NApOls[7][1] = NBLDist
            elif CN == 3 or CN == 4:
                NApOls = []
                
                for i in Surfaces:
                    NApOls.append(AppOLS[8][i])
                if NBLDist <= NApOls[7][1]:
                    NApOls[7][1] = NBLDist
                
        if NIns == 'Y':
            if NPrc == 'Y2' or NPrc == 'Y3':
                if CN == 3 or CN == 4:
                    NApOls = []
                    for i in Surfaces:
                        NApOls.append(AppOLS[9][i])         




        if STOIns == 'N':
            if CN == 2:
                SToOls = []
                for i in ToSurfs:
                    SToOls.append(ToOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            SToOls = []
                            for i in ToSurfs:
                                SToOls.append(ToOLS[1][i])                            
                else:
                    SToOls = []
                    for i in ToSurfs:
                        SToOls.append(ToOLS[0][i])
            if CN == 3 or CN == 4:
                SToOls = []
                for i in ToSurfs:
                    SToOls.append(ToOLS[2][i])
                if SMTOW22700kg == 'N' and DayOnly == 'Y':
                    SToOls[0] = 90
                if STOTurn15d == 'N' and DayOnly == 'Y':
                    SToOls[3] = 1200
        if STOIns == 'Y':
            if CN == 2:
                SToOls = []
                for i in ToSurfs:
                    SToOls.append(ToOLS[1][i])
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            SToOls = []
                            for i in ToSurfs:
                                SToOls.append(ToOLS[1][i])                            
                else:
                    SToOls = []
                    for i in ToSurfs:
                        SToOls.append(ToOLS[0][i])
            if CN == 3 or CN == 4:
                SToOls = []
                for i in ToSurfs:
                    SToOls.append(ToOLS[2][i])                



        if SIns == 'N':
            if CN == 2:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[1][i]) 
            if CN == 1:
                if DayOnly == 'N':
                    if MTOW5700kg == 'Y':
                        if RPT == 'Y':
                            SApOls = []
                            for i in Surfaces:
                                SApOls.append(AppOLS[1][i])
                else:
                    SApOls = []
                    for i in Surfaces:
                        SApOls.append(AppOLS[0][i])                         
            if CN == 3:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[2][i])
                if RWY_WID <= 30:
                    SApOls[3][0] = 90
            if CN == 4:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[3][i])
        if SIns == 'Y' and SPrc == 'N':
            if CN == 1 or CN == 2:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[4][i])            
            if CN == 3:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[5][i])
            if CN == 4:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[6][i])
                    
        if SIns == 'Y' and SPrc == 'Y1':
            if CN == 1 or CN == 2:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[7][i])
                SApOls[7][1] = SBLDist            
            if CN == 3 or CN == 4:
                SApOls = []
                for i in Surfaces:
                    SApOls.append(AppOLS[8][i])
                if SBLDist <= SApOls[7][1]:
                    SApOls[7][1] = SBLDist
        if SIns == 'Y':
            if SPrc == 'Y2' or SPrc == 'Y3':
                if CN == 3 or CN == 4:
                    SApOls = []
                    for i in Surfaces:
                        SApOls.append(AppOLS[9][i])


        #####################################################
        ## Finish configuring settings based on OLS rules ###
        #####################################################



    accur    = input("Insert size of surface cells in metres (i.e. enter a, such that cell = a*a): ")
    colour = "19ff0011"


	######################################################
    ## This part starts constructing the KML text that 
    ## will be written to a KML file
    ######################################################
    f.write("""<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom"><Document><ScreenOverlay><name>Legend: Runway Data</name><visibility>1</visibility>"""
    # """<Icon><href>[enter logo url to image here]</href></Icon>"""
    """<overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/><screenXY x="25" y="95" xunits="pixels" yunits="pixels"/><rotationXY x="0.5" y="0.5" xunits="fraction" yunits="fraction"/><size x="0" y="0" xunits="pixels" yunits="pixels"/><styleUrl>#KMLStyler</styleUrl><ExtendedData><SchemaData schemaUrl="#NewFeatureType">""")
    f.write('<SimpleData name="Airport name">'+str(KML_NAME)+'</SimpleData>\n')
    #print CN, CL
    try:
        f.write('<SimpleData name="Code">'+str(int(CN))+str(CL)+'</SimpleData>\n')
    except:
        f.write('<SimpleData name="Code">'+str(CN)+str(CL)+'</SimpleData>\n')
    f.write('<SimpleData name="Runway Length (m)">'+str(round(RwyLen,2))+'</SimpleData>\n')		
    f.write('<SimpleData name="Reference Elevation Datum (m)">'+str(RED)+'</SimpleData>\n')	
    f.write('<SimpleData name="ARP UTM (m)"> Zone '+str(zone)+"\n E="+str(ARPE)+"\n N="+str(ARPN)+'</SimpleData>\n')
    f.write('<SimpleData name="ARP Elevation (m)">'+str(ARP)+'</SimpleData>\n')
    f.write('<SimpleData name="North Approach">'+SRunwayInfo+'</SimpleData>\n')
    f.write('<SimpleData name="North Threshold UTM (m)"> Zone '+str(zone)+"\n E="+str(NTE)+"\n N="+str(NTN)+'</SimpleData>\n')
    f.write('<SimpleData name="North Threshold Elev (m)">'+str(NE)+'</SimpleData>\n')
    f.write('<SimpleData name="South Approach ">'+NRunwayInfo+'</SimpleData>\n')
    f.write('<SimpleData name="South Threshold UTM (m)"> Zone '+str(zone)+"\n E="+str(STE)+"\n N="+str(STN)+'</SimpleData>\n')
    f.write('<SimpleData name="South Threshold Elevation (m)">'+str(SE)+'</SimpleData>\n')				
    f.write('</SchemaData></ExtendedData></ScreenOverlay>\n')
    f.write('<name>'+ip.KML_NAME+'</name>\n')
    f.write('<StyleMap id="m_ylw-pushpin">\n')
    f.write('<Pair>\n')
    f.write('<key>normal</key>\n')
    f.write('<styleUrl>#s_ylw-pushpin</styleUrl>\n')
    f.write('</Pair>\n')
    f.write('<Pair>\n')
    f.write( '<key>highlight</key>\n')
    f.write( '<styleUrl>#s_ylw-pushpin_hl</styleUrl>\n')
    f.write( '</Pair>\n')
    f.write( '</StyleMap>\n')

    f.write( '<Style id="s_ylw-pushpin_hl">\n')
    f.write( '<IconStyle>\n')
    f.write( '<scale>1.3</scale>\n')
    f.write( '<Icon>\n')
    f.write( '<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>\n')
    f.write( '</Icon>\n')
    f.write( '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n')
    f.write( '</IconStyle>\n')
    f.write( '<PolyStyle>\n')
    f.write( '<color>'+colour+'</color>\n')
    f.write( '</PolyStyle>\n')
    f.write( '</Style>\n')

    f.write( '<Style id="s_ylw-pushpin">\n')
    f.write( '<IconStyle>\n')
    f.write( '<scale>1.1</scale>\n')
    f.write( '<Icon>\n')
    f.write( '<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>\n')
    f.write( '</Icon>\n')
    f.write( '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n')
    f.write( '</IconStyle>\n')

    f.write( '<PolyStyle>\n')
    f.write( '<color>'+colour+'</color>\n')
    f.write( '</PolyStyle>\n')

    f.write( '</Style>\n')

##    ObsData.Obs()

    ###############################################################
    ## This part builds the folders that make up the OLS surfaces
    ###############################################################

    if CN == 'ALA':
        ###########################################################
        ## First, if CN (Code Number) is 'ALA', where normal 
        ## airport standards don't apply, then prepare these 
        ## surfaces.
        ###########################################################

        f.write('<Folder>\n')
        f.write('<name>Approach/Take-off</name>\n')
        CAAP92App.ApN(accur)
        CAAP92App.ApS(accur)
        f.write('</Folder>\n')

        f.write('<Folder>\n')
        f.write('<name>Transitional</name>\n')
        CAAP92Trans.ApTransN(accur)
        CAAP92Trans.ApTransS(accur)
        f.write('</Folder>\n')
    else:

        ############################################################
        ## Prepare the OLS surfaces in separate KML folders below.
        ## Comment / uncomment any folders you want to include
        ## or exclude accordingly.
        ############################################################

        ## This is the Approach surface folder
        f.write('<Folder>\n')
        f.write('<name>Approach</name>\n')
        App.NorthApp(NApOls,accur)
        App.SouthApp(SApOls,accur)
        f.write('</Folder>\n')
		
        ## This is the Transitional surface folder
        f.write('<Folder>\n')
        f.write('<name>Transitional</name>\n')        
        Trans.NorthTrans(NApOls,mdl.iN(accur))
        Trans.SouthTrans(SApOls,mdl.iS(accur))
        f.write('</Folder>\n')
        
        ## This is the Inner Horizontal surface folder.
        f.write('<Folder>\n')
        f.write('<name>Inner Horizontal</name>\n')
        IHS.NInHor(NApOls,mdl.iN(accur))
        IHS.SInHor(SApOls,mdl.iS(accur))
        f.write('</Folder>\n')
        
        ## This is the Conical surface folder
        f.write('<Folder>\n')
        f.write('<name>Conical</name>\n')
        Conl.Ncon(NApOls,mdl.iN(accur))
        Conl.Scon(SApOls,mdl.iS(accur))
        f.write('</Folder>\n')
        
        ## This is the Take off surface folder
        f.write('<Folder>\n')
        f.write('<name>Take-off</name>\n')        
        TO.NorthTO(NToOls,mdl.iN(accur))
        TO.SouthTO(SToOls,mdl.iS(accur))
        f.write('</Folder>\n')
        
        ## This are the North precision surface folders
        f.write('<Folder>\n')
        f.write('<name>North Precision</name>\n')
        if NIns == 'Y':
            if NPrc != 'N':
                f.write('<Folder>\n')
                f.write('<name>Inner Approach</name>\n')
                InApp.NInApp(NApOls,mdl.iN(accur))
                f.write('</Folder>\n')
                
                f.write('<Folder>\n')
                f.write('<name>Inner Transitional</name>\n')
                InTrans.NInTrans(NApOls,mdl.iN(accur))
                f.write('</Folder>\n')
                
                f.write('<Folder>\n')
                f.write('<name>Baulked Landing</name>\n')
                Baulked.NBaulked(NApOls,mdl.iN(accur))
                f.write('</Folder>\n')
        f.write('</Folder>\n')
        
        ## These are the South Precision surface folders
        f.write('<Folder>\n')
        f.write('<name>South Precision</name>\n')            
        if SIns == 'Y':
            if SPrc != 'N':
                f.write('<Folder>\n')
                f.write('<name>Inner Approach</name>\n')
                InApp.SInApp(SApOls,mdl.iS(accur))
                f.write('</Folder>\n')
                
                f.write('<Folder>\n')
                f.write('<name>Inner Transitional</name>\n')
                InTrans.SInTrans(SApOls,mdl.iS(accur))
                f.write('</Folder>\n')
                
                f.write('<Folder>\n')
                f.write('<name>Baulked Landing</name>\n')
                Baulked.SBaulked(SApOls,mdl.iS(accur))
                f.write('</Folder>\n')
        f.write('</Folder>\n')
		
		
		
		

##        if SApOls[0][0] > 0 or NApOls[0][0] > 0:
##            ApOlsARP=[150,15000]
##            OHS.OHSSurf(ARPCoords,ApOlsARP,mdl.iN(accur))
##        

        
    f.write( '</Document>\n')
    f.write( '</kml>\n')

    ############################################################
    ## Finish writing the KML text to file. Now start the file
    ## in Google Earth.
    ###########################################################

    #f.close()
    os.startfile(completeName)
    #print 'OK, done now'


