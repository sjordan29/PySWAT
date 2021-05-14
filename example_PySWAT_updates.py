# Import pyswat - must be in working directory
import pyswat as ps

# connect to SWAT model 
model = ps.connect(r"TxtInOut")

# run SWAT
model.run(swat_version='670_rel_64')

# updated resultFile_toSQL
model.resultFile_toSQL(startDate="1989-01-01", 
                       endDate="2018-12-31", 
                       julian=True, 
                       output="swat_db.sqlite", 
                       fetch_tables=['rch', 'sub', 'hru', 'rsv'])


# expressResults
# Reach
rch_df = model.expressResults(startDate="1989-01-01", 
                              endDate="2018-12-31", 
                              id_no = 1, 
                              variable='FLOW_INcms', 
                              julian=True, 
                              fetch_tables='rch', 
                              freq='d')
# Subbasin
sub_df = model.expressResults(startDate="1989-01-01", 
                              endDate="2018-12-31", 
                              id_no=1, 
                              varialbe='PRECIPmm', 
                              julian=True, 
                              fetch_tables='sub', 
                              freq='d')
# HRU
hru_df = model.expressResults(startDate="1989-01-01", 
                              endDate="2018-12-31", 
                              id_no=300, 
                              variable='PRECIPmm', 
                              julian=True, 
                              fetch_tables='hru', 
                              freq='d')
#Reservoir
rsv_df = model.expressResults(startDate="1989-01-01", 
                              endDate="2018-12-31", 
                              id_no=3,  
                              variable="VOLUMEm3",
                              julian=True, 
                              fetch_tables='rsv', 
                              freq='d')



# Timing Tests  
import pandas as pd
import os

def timingTest(ext, ids, vbls, n_vbl, n_id):
    id_sub = ids[0:n_id]
    vb_sub = vbls[0:n_vbl]
    i = 0
    times = []
    while i < 100:
        df, t = model.expressResults("1989-01-01", "2018-12-31", id_sub, vb_sub, julian=True, fetch_tables=ext, freq='d')
        times.append(t)
        i+=1
    df = pd.DataFrame({'time': times})
    df.to_csv(os.path.join('../TimingTests', ext, 'V%sI%s.csv'%(n_vbl, n_id)))

def fullTimingTestCSV(ext, ids, vbls):
    from timeit import default_timer as timer
    i = 0
    times = []
    while i < 10:
        s = timer()
        df, t = model.expressResults("1989-01-01", "2018-12-31", ids, vbls, julian=True, fetch_tables=ext, freq='d')
        # times.append(t)
        i+=1
        for d in df:
            df[d].to_csv("AllData_%s" %i)
        e = timer()
        t = e-s
        times.append(t)
    df = pd.DataFrame({'time': times})
    df.to_csv(os.path.join('../TimingTests', ext, 'AllVariablesIDs_toCSV.csv'))
              

def fullTimingTest(ext, ids, vbls):
    times = []
    i=0
    while i < 10:
        df, t = model.expressResults("1989-01-01", "2018-12-31", ids, vbls, julian=True, fetch_tables=ext, freq='d')
        times.append(t)
        i+=1
        for d in df:
            df[d].to_csv("AllData_%s" %i)
    df = pd.DataFrame({'time': times})
    df.to_csv(os.path.join('../TimingTests', ext, 'AllVariablesIDs.csv'))



# rch 
for v in range(1,6):
    for i in range(1,6):
        timingTest('rch',  [1,15,17,20, 23], ["FLOW_OUTcms", 'FLOW_INcms','ORGN_INkg', 'CBOD_INkg', 'BURYPSTmg'], v, i)
fullTimingTest('rch', [f for f in range(1,28)], ['RCH ', 'GIS', 'MO', 'AREAkm2', 'FLOW_INcms', 'FLOW_OUTcms', 'EVAPcms', 'TLOSScms', 'SED_INtons', 'SED_OUTtons', 'SEDCONCmg/L', 'ORGN_INkg', 'ORGN_OUTkg', 'ORGP_INkg', 'ORGP_OUTkg', 'NO3_INkg', 'NO3_OUTkg', 'NH4_INkg', 'NH4_OUTkg', 'NO2_INkg', 'NO2_OUTkg', 'MINP_INkg', 'MINP_OUTkg', 'CHLA_INkg', 'CHLA_OUTkg', 'CBOD_INkg', 'CBOD_OUTkg', 'DISOX_INkg', 'DISOX_OUTkg', 'SOLPST_INmg', 'SOLPST_OUTmg', 'SORPST_INmg', 'SORPST_OUTmg', 'REACTPSTmg', 'VOLPSTmg', 'SETTLPSTmg', 'RESUSP_PSTmg', 'DIFFUSEPSTmg', 'REACBEDPSTmg', 'BURYPSTmg', 'BED_PSTmg', 'BACTP_OUTct', 'BACTLP_OUTct', 'CMETAL#1kg', 'CMETAL#2kg', 'CMETAL#3kg', 'TOT Nkg', 'TOT Pkg', 'NO3ConcMg/l', 'WTMPdegc'])

# hru
for v in range(2,6):
    for i in range(1,6):
        timingTest('hru',  [1,50,100,150,200], ["IRRmm", 'SW_ENDmm','SURQ_GENmm', 'TMP_MNdgC', 'SOLARMJ/m2'], v, i)
fullTimingTest('hru', [f for f in range(1,324)], ['LULC', 'HRU', 'GIS', 'SUB', 'MGT', 'MO', 'AREAkm2', 'PRECIPmm', 'SNOFALLmm', 'SNOMELTmm', 'IRRmm', 'PETmm', 'ETmm', 'SW_INITmm', 'SW_ENDmm', 'PERCmm', 'GW_RCHGmm', 'DA_RCHGmm', 'REVAPmm', 'SA_IRRmm', 'DA_IRRmm', 'SA_STmm', 'DA_STmm', 'SURQ_GENmm', 'SURQ_CNTmm', 'TLOSSmm', 'LATQGENmm', 'GW_Qmm', 'WYLDmm', 'DAILYCN', 'TMP_AVdgC', 'TMP_MXdgC', 'TMP_MNdgC', 'CSOL_TMPdgC', 'SOLARMJ/m2', 'SYLDt/ha', 'USLEt/ha', 'N_APPkg/haP', 'P_APPkg/ha', 'NAUTOkg/ha', 'PAUTOkg/ha', 'NGRZkg/ha ', 'PGRZkg/ha', 'NCFRTkg/ha', 'PCFRTkg/ha', 'NRAINkg/ha', 'NFIXkg/ha', 'F-MNkg/ha', 'A-MNkg/ha', 'A-SNkg/ha', 'F-MPkg/ha', 'AO-LPkg/ha', 'L-APkg/ha', 'A-SPkg/ha', 'DNITkg/ha', 'NUPkg/ha', 'PUPkg/ha', 'ORGNkg/ha', 'ORGPkg/ha', 'SEDPkg/ha', 'NSURQkg/ha', 'NLATQkg/ha', 'NO3Lkg/ha', 'NO3GWkg/ha', 'SOLPkg/ha', 'P_GWkg/ha', 'W_STRS', 'TMP_STRS', 'N_STRS', 'P_STRS', 'BIOMt/ha', 'LAI', 'YLDt/ha', 'BACTPct', 'BACTLPct', 'WTAB CLIm', 'WTAB SOLm', 'SNOmm', 'CMUPkg/ha', 'CMTOTkg/ha', 'QTILEmm', 'TNO3kg/ha', 'LNO3kg/ha', 'GW_Q_Dmm', 'LATQCNTmm', 'TVAPkg/ha'])

# rsv
for v in range(1,6):
    for i in range(1,4):
        timingTest('rsv',  [1,3,4], ["VOLUMEm3", 'EVAPm3','MINP_INkg', 'VOLPSTmg', 'PEST_OUTmg'], v, i)
fullTimingTest('rsv', [1,3,4], ['RES', 'MON', 'VOLUMEm3', 'FLOW_INcms', 'FLOW_OUTcms', 'PRECIPm3', 'EVAPm3', 'SEEPAGEm3', 'SED_INtons', 'SED_OUTtons', 'SED_CONCppm', 'ORGN_INkg', 'ORGN_OUTkg', 'RES_ORGNppm', 'ORGP_INkg', 'ORGP_OUTkg', 'RES_ORGPppm', 'NO3_INkg', 'NO3_OUTkg', 'RES_NO3ppm', 'NO2_INkg', 'NO2_OUTkg', 'RES_NO2ppm', 'NH3_INkg', 'NH3_OUTkg', 'RES_NH3ppm', 'MINP_INkg', 'MINP_OUTkg', 'RES_MINPppm', 'CHLA_INkg', 'CHLA_OUTkg', 'SECCHIDEPTHm', 'PEST_INmg', 'REACTPSTmg', 'VOLPSTmg', 'SETTLPSTmg', 'RESUSP_PSTmg', 'DIFFUSEPSTmg', 'REACBEDPSTmg', 'BURYPSTmg', 'PEST_OUTmg', 'PSTCNCWmg/m3', 'PSTCNCBmg/m3'])  


# sub
for v in range(1,6):
    for i in range(1,6):
        timingTest('sub',  [1,15,17,20, 23], ['PRECIPmm', 'GW_Qmm','ORGNkg/ha', 'SEDPkg/ha', 'DOXQ mg/L'], v, i)
fullTimingTest('sub', [f for f in range(1,28)], ['SUB', 'GIS', 'MO', 'AREAkm2', 'PRECIPmm', 'SNOMELTmm', 'PETmm', 'ETmm', 'SWmm', 'PERCmm', 'SURQmm', 'GW_Qmm', 'WYLDmm', 'SYLDt/ha', 'ORGNkg/ha', 'ORGPkg/ha', 'NSURQkg/ha', 'SOLPkg/ha', 'SEDPkg/ha', 'LAT Q(mm)', 'LATNO3kg/h', 'GWNO3kg/ha', 'CHOLAmic/L', 'CBODU mg/L', 'DOXQ mg/L', 'TNO3kg/ha', 'QTILEmm', 'TVAPkg/ha'])  
   
 
 

# Timing test: all variables, all subbasins - include timing of save to csv files 
fullTimingTestCSV('rch', [f for f in range(1,28)], ['RCH ', 'GIS', 'MO', 'AREAkm2', 'FLOW_INcms', 'FLOW_OUTcms', 'EVAPcms', 'TLOSScms', 'SED_INtons', 'SED_OUTtons', 'SEDCONCmg/L', 'ORGN_INkg', 'ORGN_OUTkg', 'ORGP_INkg', 'ORGP_OUTkg', 'NO3_INkg', 'NO3_OUTkg', 'NH4_INkg', 'NH4_OUTkg', 'NO2_INkg', 'NO2_OUTkg', 'MINP_INkg', 'MINP_OUTkg', 'CHLA_INkg', 'CHLA_OUTkg', 'CBOD_INkg', 'CBOD_OUTkg', 'DISOX_INkg', 'DISOX_OUTkg', 'SOLPST_INmg', 'SOLPST_OUTmg', 'SORPST_INmg', 'SORPST_OUTmg', 'REACTPSTmg', 'VOLPSTmg', 'SETTLPSTmg', 'RESUSP_PSTmg', 'DIFFUSEPSTmg', 'REACBEDPSTmg', 'BURYPSTmg', 'BED_PSTmg', 'BACTP_OUTct', 'BACTLP_OUTct', 'CMETAL#1kg', 'CMETAL#2kg', 'CMETAL#3kg', 'TOT Nkg', 'TOT Pkg', 'NO3ConcMg/l', 'WTMPdegc'])
fullTimingTestCSV('hru', [f for f in range(1,324)], ['LULC', 'HRU', 'GIS', 'SUB', 'MGT', 'MO', 'AREAkm2', 'PRECIPmm', 'SNOFALLmm', 'SNOMELTmm', 'IRRmm', 'PETmm', 'ETmm', 'SW_INITmm', 'SW_ENDmm', 'PERCmm', 'GW_RCHGmm', 'DA_RCHGmm', 'REVAPmm', 'SA_IRRmm', 'DA_IRRmm', 'SA_STmm', 'DA_STmm', 'SURQ_GENmm', 'SURQ_CNTmm', 'TLOSSmm', 'LATQGENmm', 'GW_Qmm', 'WYLDmm', 'DAILYCN', 'TMP_AVdgC', 'TMP_MXdgC', 'TMP_MNdgC', 'CSOL_TMPdgC', 'SOLARMJ/m2', 'SYLDt/ha', 'USLEt/ha', 'N_APPkg/haP', 'P_APPkg/ha', 'NAUTOkg/ha', 'PAUTOkg/ha', 'NGRZkg/ha ', 'PGRZkg/ha', 'NCFRTkg/ha', 'PCFRTkg/ha', 'NRAINkg/ha', 'NFIXkg/ha', 'F-MNkg/ha', 'A-MNkg/ha', 'A-SNkg/ha', 'F-MPkg/ha', 'AO-LPkg/ha', 'L-APkg/ha', 'A-SPkg/ha', 'DNITkg/ha', 'NUPkg/ha', 'PUPkg/ha', 'ORGNkg/ha', 'ORGPkg/ha', 'SEDPkg/ha', 'NSURQkg/ha', 'NLATQkg/ha', 'NO3Lkg/ha', 'NO3GWkg/ha', 'SOLPkg/ha', 'P_GWkg/ha', 'W_STRS', 'TMP_STRS', 'N_STRS', 'P_STRS', 'BIOMt/ha', 'LAI', 'YLDt/ha', 'BACTPct', 'BACTLPct', 'WTAB CLIm', 'WTAB SOLm', 'SNOmm', 'CMUPkg/ha', 'CMTOTkg/ha', 'QTILEmm', 'TNO3kg/ha', 'LNO3kg/ha', 'GW_Q_Dmm', 'LATQCNTmm', 'TVAPkg/ha'])
fullTimingTestCSV('rsv', [1,3,4], ['RES', 'MON', 'VOLUMEm3', 'FLOW_INcms', 'FLOW_OUTcms', 'PRECIPm3', 'EVAPm3', 'SEEPAGEm3', 'SED_INtons', 'SED_OUTtons', 'SED_CONCppm', 'ORGN_INkg', 'ORGN_OUTkg', 'RES_ORGNppm', 'ORGP_INkg', 'ORGP_OUTkg', 'RES_ORGPppm', 'NO3_INkg', 'NO3_OUTkg', 'RES_NO3ppm', 'NO2_INkg', 'NO2_OUTkg', 'RES_NO2ppm', 'NH3_INkg', 'NH3_OUTkg', 'RES_NH3ppm', 'MINP_INkg', 'MINP_OUTkg', 'RES_MINPppm', 'CHLA_INkg', 'CHLA_OUTkg', 'SECCHIDEPTHm', 'PEST_INmg', 'REACTPSTmg', 'VOLPSTmg', 'SETTLPSTmg', 'RESUSP_PSTmg', 'DIFFUSEPSTmg', 'REACBEDPSTmg', 'BURYPSTmg', 'PEST_OUTmg', 'PSTCNCWmg/m3', 'PSTCNCBmg/m3'])  
fullTimingTestCSV('sub', [f for f in range(1,28)], ['SUB', 'GIS', 'MO', 'AREAkm2', 'PRECIPmm', 'SNOMELTmm', 'PETmm', 'ETmm', 'SWmm', 'PERCmm', 'SURQmm', 'GW_Qmm', 'WYLDmm', 'SYLDt/ha', 'ORGNkg/ha', 'ORGPkg/ha', 'NSURQkg/ha', 'SOLPkg/ha', 'SEDPkg/ha', 'LAT Q(mm)', 'LATNO3kg/h', 'GWNO3kg/ha', 'CHOLAmic/L', 'CBODU mg/L', 'DOXQ mg/L', 'TNO3kg/ha', 'QTILEmm', 'TVAPkg/ha'])  

  



 