# PySWAT is a Command Line Interface(CLI) for Input/Output manipulation and analysis of the Soil and Water Assessment Tool(SWAT). 

PySWAT Couples SWAT to the Power of Python Language to connect SWAT 
Input/Output Data to Powerful Python Libraries such as SQLite, Pandas,
Numpy and MatplotLib

Features can be used to assess output data, generate 
graphs, perform custom queries and much more!

Original Author: David Bispo Ferreira - Federal University of Parana - 2017
Contributions by Sarah Jordan - University of Virginia - 2021


# QuickStart

## 1. Get Anaconda at [Anaconda's Website](https://www.anaconda.com/distribution/#download-secion)
*If you are not a first timer with python, use the way you know best! You need matplotlib, pandas, numpy and SQlite, which are covered by anaconda.

## 2. Open Spyder, Anaconda's IDE
Connect your Project to pySWAT

## 3. Create a python file in the same folder as pySWAT 

## 4. Explore your data


# Contributions to PySWAT
There are multiple new features in this updated version of PySWAT with the aim of improving the reproducibility, capabilities, and speed of PySWAT:
* Flexibility to date format in the output files
* Ability to process reservoir output files (output.rsv) 
* Addition of the *expressResults* function, a faster option for extracting data from output files 

## Examples of PySWAT Updates in Action:

### Updates to *resultFile_toSQL* function

*resultFile_toSQL* works the same as it did before, but in includes three additional input parameters:
* **startDate: _str or datetime-like object_:** specifies the date when the model output begins to be printed to output files (after the warm-up period)
* **endDate: _str or datetime-like object_:** specifies the end date of the simulation
* **julian: _bool, default=False_:** Identifies if dates in the model output are in month, day, and year format (False) or Julian format (True)
* **freq: _str or DateOffset, default='d'_:** Output  frequency.  Can  be  ‘d’  for  daily,  ‘M’  formonthly, or ‘A’ for annual


```python
# Import pyswat - must be in working directory
import pyswat as ps

# connect to SWAT model 
model = ps.connect(r"TxtInOut")

# run SWAT
model.run(swat_version='670_rel_64')

# updated resultFile_toSQL
model.resultFile_toSQL(startDate="1989-01-01", # new input parameter
                       endDate="2018-12-31",  # new input parameter
                       julian=True, # new input parameter
                       output="swat_db.sqlite", 
                       fetch_tables=['rch', 'sub', 'hru', 'rsv'])

```

### Updates to *expressResults* function
*expressResults* contains many of the same input parameters as *resultFile_toSQL* (*startDate, endDate, julian, fetch_tables, freq*), but it also includes:
* **id_no: _int or list of int_:** Unique identifier(s) of reach(es), subbasin(s), HRU(s), or reservoir(s) of interest
* **variable: _str or list of str_:** Variable(s) of interest. The names are the same as detailed in Chapter 32 of the SWAT User's Manual, both in terms of capitalization and special characters. 

```python
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


```