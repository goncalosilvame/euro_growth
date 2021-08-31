"""
Created on Sat Aug 28 11:35:39 2021
@author: JGSILVA

This file creates the dataset to use further.
Input : Source csvs
Output: database.csv
"""

#%% Get directory
import os
print(os.getcwd())

# Packages
import pandas as pd
import numpy as np

#%% Load data
gdp_ppp = pd.read_csv("Data/gdp_ppp.csv")
df_1 = pd.read_csv("Data/gdp_ppp.csv", index_col=[0,5], skipinitialspace=True)
population = pd.read_csv("Data/population.csv")
working_age = pd.read_csv("Data/working age_percentage.csv")
inflation = pd.read_csv("Data/Inflation - CPI.csv")
exports = pd.read_csv("Data/Exports_gdp.csv") #percentage of gdp ?
imports = pd.read_csv("Data/Imports_gdp.csv")   #percentage of gpd?


#%% Merge data
print(gdp_ppp.columns) #check the columns to delete what I do not need.

#['LOCATION', 'INDICATOR', 'SUBJECT', 'MEASURE', 'FREQUENCY', 'TIME',
#       'Value', 'Flag Codes']

# Delete useless columns
oecd_data = [working_age, population, gdp_ppp, inflation, exports, imports]
oecd_data_s = ['working_age','population','gdp_ppp','inflation', 'exports', 'imports']
   
for i in range(0, len(oecd_data)):
    oecd_data[i].drop(['INDICATOR','SUBJECT', 'MEASURE', 'FREQUENCY', 'Flag Codes'], axis=1, inplace=True) 
    oecd_data[i].rename(columns = {'Value': oecd_data_s[i]},inplace= True)

# Merge first two to see if it is correct
# started with highest frequency data. 
df = working_age.merge(population, how= 'left', on=['LOCATION','TIME'])

# Merge the other ones
for i in range(2, len(oecd_data)):
    df = df.merge(oecd_data[i], how= 'left', on=['LOCATION','TIME'])

#%% Create dummy variables.
codes = ['AUT', 'BEL', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 
            'FRA', 'DEU', 'GRC', 'HUN', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 
            'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP', 'SWE']

codes_ea = ['AUT', 'BEL', 'CYP',  'EST', 'FIN', 
            'FRA', 'DEU', 'GRC', 'IRL', 'ITA' ,'LVA', 'LTU', 'LUX', 
            'MLT', 'NLD',  'PRT', 'SVK', 'SVN', 'ESP']


codes_eu = pd.DataFrame(np.array(codes), columns = [ "LOCATION"])
codes_ea = pd.DataFrame(np.array(codes_ea), columns = [ "LOCATION"])
codes_eu['eu'] = 1
codes_ea['ea']=1
# codes_eu.rename(columns = {'0': 'LOCATION'})

df = df.merge(codes_eu, how = "left", on = 'LOCATION')
df = df.merge(codes_ea, how = "left", on = 'LOCATION')

#replace missing values for dummie for 0
df['eu'] = df['eu'].fillna(0)
df['ea'] = df['eu'].fillna(0)
#%% Export
df.to_csv('Data/database.csv', index =False)
 
