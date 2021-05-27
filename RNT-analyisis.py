# conda install -c conda-forge tabula-py
import tabula
import pandas as pd
import numpy as np
import sys
import os.path

# Usage python3.X RNT-analyisis.py RNT_YYYYMM.pdf
# Output analysis_RNT_YYYYMM.xlsx

# Read PDF into list of DataFrame

def isNaN(string):
    return string != string

input_RNT=sys.argv[1] # Argument must be given as RNT_YYYYMM.pdf
input_workers=sys.argv[2]

dataframe = tabula.read_pdf(input_RNT, pages='all', multiple_tables=True, lattice=True)
workers = pd.read_excel(input_workers)
reference_period = os.path.basename(input_RNT)[4:10]

data=pd.DataFrame() # Dataframe with workers data

#Extract from the .pdf only the tables with the workers' data.

for i in np.arange(0,len(dataframe)):
    if dataframe[i].shape[1] > 9:
        data_each=pd.DataFrame(dataframe[i])
        data=data.append(data_each, sort=False)

data.dropna(subset = ["Días\rCoti."], inplace=True) # Drop lines which do not contain anything in the Dias Coti column
data = data.loc[data["Días\rCoti."].str.contains("[0-9] D")] # The expected value is something like "30 D"
data = data.reset_index() # Important! The indexes are the original ones from the single pages and need to be updated
# Generate a dataframe which will be printed in the excel output file.

#id_workers=pd.DataFrame(np.zeros((len(workers),4)), columns = ["Nombre Completo", "CAF", "Base / €", "Anual / €"])
workers[reference_period] = np.zeros((len(workers),1))
days_in_the_month = 30 # seems they're always "30 D" but very randomly can be 31 for individuals
#days_in_the_month = max(pd.to_numeric(data["Días\rCoti."].str.replace(" D","")))

for i in np.arange(0,len(workers)):
    #name_id=workers["Nombre Completo"].loc[i] # Read the name of each worker
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
    index = -1
    indexes = data.index[data["C.A.F."] == caf].tolist() # Get the line number of the CAF matches
   # print(data["C.A.F."] == caf)
    if len(indexes) == 0: # To make sure the worker exists!
        base="CAF not found, check manually!" # The worker does not exists / its generated CAF is wrong.
    elif len(indexes) == 1:
        index = indexes[0]
    elif not isNaN(ipf): # More than one correspondency for one CAF and IPF exists
        indexes = data.index[data["I.P.F."] == ipf].tolist() # Get the line number of the IPF matches
        if len(indexes) == 1: # One correspondency with IPF
            index = indexes[0]
        else:
            base="CAF not found and IPF not found or duplicated, check manually!"
    else:
        base="Double CAF and missing IPF, check manually!"
    if index >= 0: # Check that previous code found the line
        num_to_clean=data.iloc[index,10] # Print the BASE DE CONTINGENCIAS COMUNE
        pos_r=num_to_clean.find('\r') # Clean its format
        base=float(num_to_clean[0:pos_r].replace(",",""))/100 # Convert it to a number
        days = int(data["Días\rCoti."].iloc[index].replace(" D","")) # Take out the number of days from "30 D"
        daily = base / days
        anual = daily * days_in_the_month * 12 # Get the annual value
        if anual >= 48841.2: 
            anual="> 48841.2" # Correct the annual value for the highest threshold.
        
    #id_workers.iloc[i,:]=[name_id,caf,base,anual,0] # Print the values for the excel
    workers.iloc[i, workers.columns.get_loc(reference_period)] = anual
workers.to_excel("analysis_RNT_"+reference_period+".xlsx", index=False) # Generate the excel.
