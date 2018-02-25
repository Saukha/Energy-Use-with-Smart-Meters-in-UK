import pandas as pd
import numpy as np
import matplotlib
import datetime

# data filenames
# energy usage files cols = 'LCLid', 'DateTime', 'KWH/hh (per half hour) '
datafile_list=['block_0.csv', 'block_1.csv', 'block_2.csv', 'block_3.csv', 'block_4.csv', 'block_5.csv',  'block_6.csv', 'block_7.csv', 'block_8.csv', 'block_9.csv', 'block_10.csv', 'block_11.csv', 'block_12.csv', 'block_13.csv', 'block_14.csv']
#datafile_list=['block_14.csv']
# create csv lising each smart meter user and mean half hour electricity usage
for filename in datafile_list:
    df=pd.read_csv(filename)    
    s1=df.groupby('LCLid')['KWH/hh (per half hour) '].mean()
    s1.to_csv('Mean_KWH_perhh_'+filename)
    s2=df.groupby('LCLid')['KWH/hh (per half hour) '].sum()
    s2.to_csv('Total_KWH_perhh_'+filename)
    df.DateTime=pd.to_datetime(df.DateTime)
    s3=df.groupby('LCLid')['DateTime'].min()
    s3.to_csv('Start_'+filename)
    s4=df.groupby('LCLid')['DateTime'].max()
    s4.to_csv('End_'+filename)

for filename in datafile_list:
    file1='Start_'+filename
    file2='End_'+filename
    file3='Total_KWH_perhh_'+filename
    file4='Mean_KWH_perhh_'+filename
    df1=pd.read_csv(file1, names=['LCLid','Start'])
    df2=pd.read_csv(file2, names=['LCLid','End'])
    df3=pd.read_csv(file3, names=['LCLid','Total_Usage_KWH'])
    df4=pd.read_csv(file4, names=['LCLid','Mean_Usage_KWH/hh'])
    df5=pd.merge(left=df1, right=df2, how='left', left_on='LCLid',right_on='LCLid')
    df5=pd.merge(left=df5, right=df3, how='left', left_on='LCLid',right_on='LCLid')
    df5=pd.merge(left=df5, right=df4, how='left', left_on='LCLid',right_on='LCLid')
    df5.to_csv('summary_'+filename)       
    print filename

# compile final summary file
new_datafile_list=['block_1.csv', 'block_2.csv', 'block_3.csv', 'block_4.csv', 'block_5.csv',  'block_6.csv', 'block_7.csv', 'block_8.csv', 'block_9.csv', 'block_10.csv', 'block_11.csv', 'block_12.csv', 'block_13.csv', 'block_14.csv']
df8=pd.read_csv('summary_block_0.csv')
for filename in new_datafile_list:
    df9=pd.read_csv('summary_'+filename)
    df8=pd.concat([df8,df9],axis=0)
    df8.dropna(inplace=True)
    df8.to_csv('summary_all_blocks.csv')    

df8=pd.read_csv('summary_all_blocks.csv')
df6=pd.read_csv('informations_household_update.csv',na_values=['ACORN-', 'ACORN-U',' ','Null','null','N/A','na','',float('inf'), float('-inf'), np.inf, -np.inf])      
df.dropna(inplace=True)
df9=pd.merge(left=df8, right=df6, how='left', left_on='LCLid', right_on='LCLid')
df9.to_csv('New_summary_with_household_info.csv')

