# conda install -c conda-forge tabula-py
import tabula
import pandas as pd
import numpy as np
import sys

# Usage python3.X RNT-analyisis.py RNT_YYYYMM.pdf
# Output analysis_RNT_YYYYMM.xlsx

# Read PDF into list of DataFrame

def isNaN(string):
    return string != string

input=sys.argv[1] # Argument must be given as RNT_YYYYMM.pdf 

dataframe = tabula.read_pdf(input, pages='all', multiple_tables=True, lattice=True)
workers = pd.read_excel('Trabajadores con relacion laboral y CAF.xls')

data=pd.DataFrame() # Dataframe with workers data

#Extract from the .pdf only the tables with the workers' data.

for i in np.arange(0,len(dataframe)):
    if dataframe[i].shape[1] > 9:
        data_each=pd.DataFrame(dataframe[i])
        data=data.append(data_each)

data.dropna(subset = ["Días\rCoti."], inplace=True) # Drop lines which do not contain anything in the Dias Coti column
data = data.loc[data["Días\rCoti."].str.contains("[0-9] D")] # The expected value is something like "30 D"

# Generate a dataframe which will be printed in the excel output file.

id_workers=pd.DataFrame(np.zeros((len(workers),4)), columns = ["Nombre Completo", "CAF", "Base / €", "Anual / €"])

for i in np.arange(0,len(workers)):
    
    name_id=workers["Nombre Completo"].loc[i] # Read the name of each worker
    
    #The following section is to generate the CAF automatically from workers' name, if needed
    
    #comma_pos=name_id.find(',')
    #l_name=name_id[comma_pos+2]
    #l_surname_1=name_id[0:2]
    #space_pos=name_id.find(' ')

    #if space_pos != comma_pos + 1:
    #    l_surname_2=name_id[space_pos+1:space_pos+3]
    #    caf=l_surname_1+l_surname_2+l_name
    #else:
    #    caf=l_surname_1+"  "+l_name
    #    
    
    caf=workers["CAF"].loc[i] # Read the CAF of each worker
    ipf=workers["IPF"].loc[i] # Read the IPF of each worker
    anual = ""
    base = ""
    num_to_clean = ""
    if len(data[data["C.A.F."] == caf]) == 0: # To make sure the worker exists!
        base="CAF not found, check manually!" # The worker does not exists / its generated CAF is wrong.
    elif len(data[data["C.A.F."] == caf]) == 1:
        num_to_clean=data[data["C.A.F."] == caf].iloc[0,9] # Print the BASE DE CONTINGENCIAS COMUNE
    elif not isNaN(ipf): # More than one correspondency for one CAF and IPF exists
        if len(data[data["I.P.F."] == ipf]) == 1: # One correspondency with IPF
            num_to_clean=data[data["I.P.F."] == ipf].iloc[0,9] # Print the BASE DE CONTINGENCIAS COMUNE
        else:
            base="CAF not found and IPF not found or duplicated, check manually!"
    else:
        base="Double CAF and missing IPF, check manually!"
    if not len(num_to_clean) == 0: # Check that previous code filled the string
        pos_r=num_to_clean.find('\r') # Clean its format
        base=float(num_to_clean[0:pos_r].replace(",",""))/100 # Convert it to a number
        anual=base*12 # Get the annual value
        if base == 4070.1: 
            anual="> 48841.2" # Correct the annual value for the highest threshold.
        
        
    id_workers.iloc[i,:]=[name_id,caf,base,anual] # Print the values for the excel
id_workers.to_excel("analysis_RNT_"+input[4:10]+".xlsx") # Generate the excel.
