# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 13:41:21 2021
@author: JGSILVA

This file creates the variables to be used in the regression analysis.
Input: database.csv
"""

import pandas as pd
import numpy as np

#%% Setting up the panel data
# setting time and id variables
# Have to set two index variables.
    # ID = LOCATION, TIME = TIME
# # guess same logic as in Stata

df = pd.read_csv('Data/database.csv', index_col = ['LOCATION', 'TIME'])

years = df.index.get_level_values('TIME').to_list()
df['TIME'] = pd.Categorical(years)


#%% VARIABLES

# working age population
df['pop_work']= (df.population*df.working_age)

# GDP per working age:
df['gdp_per_work'] = df.gdp_ppp/df.pop_work
       
# 5 year growth rate:
df['gr5y'] = (df.gdp_per_work-df.gdp_per_work.shift(5))/df.gdp_per_work.shift(5)

#Trade_in_good
df['trade_in_goods'] = df.imports + df.exports 

# independet variables
indp = ['pop_work','gdp_per_work','trade_in_goods','inflation']


#%%

for i in  indp:
    var_a = df[i].shift(5)   
    exist = pd.notnull(df[i])
    exist = np.array(exist)
    for y in range(0, len(exist)):
        if exist[y] == True:
            var_a[y] = var_a[y]
        else:
            var_a[y] = np.nan     
    print(i)
    df[i + '_5'] =  np.array(var_a)       
    

#%% get the final dataset and export

df['years'] = np.array(years)
data_final = df.filter(items=['eu', 'ea','gr5y','pop_work_5','gdp_per_work_5','trade_in_goods_5','inflation_5', 'years'])
data_final = data_final.loc[(data_final['years'] >= 1975)]

data_final.to_csv('Data/data_final.csv',index=True)