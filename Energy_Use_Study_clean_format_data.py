import pandas as pd
import numpy as np
import matplotlib
import datetime
from matplotlib import pyplot as plt
import project3_modules as my_modules

# this code is only to plot inline in Jupyter Notebook
#%matplotlib inline 

# data filenames
fileA='informations_household_update.csv'
fileB='acorn_details.csv'

# energy usage files cols = 'LCLid', 'DateTime', 'KWH/hh (per half hour) '
datafile_list=['block_0.csv', 'block_1.csv', 'block_2.csv', 'block_3.csv', 'block_4.csv', 'block_5.csv',  'block_6.csv', 'block_7.csv', 'block_8.csv', 'block_9.csv', 'block_10.csv', 'block_11.csv', 'block_12.csv', 'block_13.csv', 'block_14.csv']

# convert csv data into DataFrame, convert datetime col from str to DateTime type, add 'Year', 'Month', 'Day_of_Week' and 'Hour' col, 
# and save each DataFrame as csv file, replacing original csv file.
for item in datafile_list: 
    my_modules.clean_format_csv(item)


for filename in datafile_list:
    df=dp.read_csv(filename)
    df.DateTime=pd.to_datetime(df.DateTime)
    df1=df.groupby('LCLid').[DateTime].min()
    df1['EndTime']=df.groupby('LCLid').[DateTime].max()
    #df['file', 'BeginDateTime', 'EndDateTime']=file, 
    print filename +": " +str(df.DateTime.min()) + ' through ' + str(df.DateTime.max())

# block_0.csv file is too big and causes memory problem during data analysis and visualization
# split block_0.csv file into two block_0-a.csv and block_0-b.csv
# final_file_list = ['block_0-a.csv', 'block_0-b.csv', 'block_1.csv', 'block_2.csv', 'block_3.csv', 'block_4.csv', 'block_5.csv', 'block_6.csv', 'block_7.csv','block_8.csv','block_9.csv','block_10.csv','block_11.csv','block_12.csv','block_13.csv','block_14.csv']
df=pd.read_csv('block_0.csv')
df1=df[df['LCLid']<'MAC000235'] # splitting by this LCLid gives appro. half the file size
df2=df[df['LCLid']>'MAC000234'] # splitting by this LCLid gives appro. half the file size
df1.to_csv('block_0-a', sep=',') # save data to csv format
df2.to_csv('block_0-b', sep=',') # save data to csv format

# clean informations_household_update.csv
df=pd.read_csv(fileA, na_values=[' ','Null','null','N/A','na','',float('inf'), float('-inf'), np.inf, -np.inf])      
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df_household_info=df[['LCLid','Acorn','Acorn_grouped']]
df_household_info.to_csv('household_shortfile.csv', sep=',') #save short household file with cleaned up version 


