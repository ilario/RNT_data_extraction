# conda install -c conda-forge tabula-py
import tabula
import pandas as pd
import numpy as np
import sys

# Usage python3.X RNT-analyisis.py RNT_YYYYMM.pdf
# Output analysis_RNT_YYYYMM.xlsx

# Read PDF into list of DataFrame

input=sys.argv[1] # Argument must be given as RNT_YYYYMM.pdf 

dataframe = tabula.read_pdf(input, pages='all', multiple_tables=True, spreadsheet=True)
workers = pd.read_excel('Trabajadores con relacion laboral y CAF.xls')

data=pd.DataFrame() # Dataframe with workers data

#Extract from the .pdf only the tables with the workers' data.

for i in np.arange(0,len(dataframe)):
    if dataframe[i].shape[1] > 9:
        data_each=pd.DataFrame(dataframe[i])
        data=data.append(data_each)
        
# Generate a dataframe which will be printed in the excel output file.

id_workers=pd.DataFrame(np.zeros((len(workers),5)), columns = ["Nombre Completo", "CAF", "Base / €", "Anual / €", "Observation"])

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
    
    if len(data[data[2] == caf]) > 0: # To make sure the worker exists!

        num_to_clean=data[data[2] == caf].iloc[0,9] # Print the BASE DE CONTINGENCIAS COMUNE 
        pos_r=num_to_clean.find('\r') # Clean its format
        base=float(num_to_clean[0:pos_r].replace(",",""))/100 # Convert it to a number
        
        anual=base*12 # Get the annual value
        if base == 4070.1: 
            anual="> 48841.2" # Correct the annual value for the highest threshold.
        
        if len(data[data[2] == caf]) > 1: # If there are two equivalent CAF, it must be checked manually.
            obs="Double CAF, check manually!"
        else:
            obs=" "
        
    else:
        base="Not found, check manually!" # The worker does not exists / its generated CAF is wrong.
        anual=" "
        obs=" "
        
    id_workers.iloc[i,:]=[name_id,caf,base,anual,obs] # Print the values for the excel
id_workers.to_excel("analysis_RNT_"+input[4:10]+".xlsx") # Generate the excel.
