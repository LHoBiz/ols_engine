##        
        f.write('<Folder>\n')
        f.write('<name>Transitional</name>\n')        
        Trans.NorthTrans(NApOls,mdl.iN(accur))
        Trans.SouthTrans(SApOls,mdl.iS(accur))
        f.write('</Folder>\n')
        
        f.write('<Folder>\n')
        f.write('<name>Inner Horizontal</name>\n')
        IHS.NInHor(NApOls,mdl.iN(accur))
        IHS.SInHor(SApOls,mdl.iS(accur))
        f.write('</Folder>\n')
        
        f.write('<Folder>\n')
        f.write('<name>Conical</name>\n')
        Conl.Ncon(NApOls,mdl.iN(accur))
        Conl.Scon(SApOls,mdl.iS(accur))
        f.write('</Folder>\n')
        
        f.write('<Folder>\n')
        f.write('<name>Take-off</name>\n')        
        TO.NorthTO(NToOls,mdl.iN(accur))
        TO.SouthTO(SToOls,mdl.iS(accur))
        f.write('</Folder>\n')
        
        f.write('<Folder>\n')
        f.write('<name>North Precision</name>\n')
        if NIns == 'Y':
            if NPrc <> 'N':
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
        
        f.write('<Folder>\n')
        f.write('<name>South Precision</name>\n')            
        if SIns == 'Y':
            if SPrc <> 'N':
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