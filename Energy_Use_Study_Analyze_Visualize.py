import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

# this code is only to plot inline in Jupyter Notebook
#%matplotlib inline 

# energy usage files cols = LCLid, DateTime, KWH/hh (per half hour)
datafile_list=['block_0.csv','block_1.csv','block_2.csv','block_3.csv','block_4.csv','block_5.csv','block_6.csv',
'block_7.csv','block_8.csv','block_9.csv','block_10.csv','block_11.csv','block_12.csv','block_13.csv','block_14.csv']

# block_0.csv file is too big and causes memory problem during data analysis and visualization
# split block_0.csv file into two block_0-a.csv and block_0-b.csv
# final_file_list = ['block_0-a.csv', 'block_0-b.csv', 'block_1.csv', 'block_2.csv', 'block_3.csv', 'block_4.csv', 'block_5.csv', 'block_6.csv', 'block_7.csv','block_8.csv','block_9.csv','block_10.csv','block_11.csv','block_12.csv','block_13.csv','block_14.csv']

# analyze and visualize data one block at a time and merge dfs 
# enter one filename at a time and run this scripts
block='block_0-b.csv'
df1=pd.read_csv(block)
df2=pd.read_csv('household_shortfile.csv', na_values=['ACORN-U','ACORN-']) # to drop incomplete entries
df2.dropna(inplace=True) 
df_merged=pd.merge(left=df1,right=df2,how='left',on='LCLid')
df_merged.dropna(inplace=True)

# create plots
s1=df_merged.groupby('Acorn_grouped',as_index=True)['KWH/hh (per half hour) '].sum()
chart1=s1.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Category")
fig1=chart1.figure 
fig1.set_size_inches(6,4)
fig1.tight_layout(pad=2)
chart1.set_xlabel('Acorn Category')
chart1.set_ylabel('Electricity Usage KWH')
fig1.savefig(block+' By Acorn Category.png',dpi=125)

s2=df_merged.groupby('Acorn',as_index=True)['KWH/hh (per half hour) '].sum()/1000000
chart2=s2.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Type")
fig2=chart2.figure 
fig2.set_size_inches(6,4)
fig2.tight_layout(pad=3)
chart2.set_xlabel('Acorn Type')
chart2.set_ylabel('Electricity Usage, x 1,000,000 KWH')
fig2.savefig(block+' By Acorn Type.png',dpi=125)

s3=df_merged.groupby(['Acorn_grouped','Month'])['KWH/hh (per half hour) '].sum()/1000000
chart3=s3.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Category By Month")
fig3=chart3.figure 
fig3.set_size_inches(20,8)
fig3.tight_layout(pad=2)
chart3.set_xlabel('Acorn Category by Month')
chart3.set_ylabel('Electricity Usage, x 1,000,000 KWH')
fig3.savefig('NEW_'+block+' By Acorn Category By Month.png',dpi=125)

s4=df_merged.groupby(['Acorn_grouped','Year'])['KWH/hh (per half hour) '].sum()
chart4=s4.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Category By Year")
fig4=chart4.figure 
fig4.set_size_inches(8,4)
fig4.tight_layout(pad=3)
chart4.set_xlabel('Acorn Category')
chart4.set_ylabel('Electricity Usage KWH')
fig4.savefig(block+' By Acorn Category By Year.png',dpi=125)

'''
s5=df_merged.groupby(['Acorn_grouped','Hour'])['KWH/hh (per half hour) '].sum()/1000000
chart5=s5.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Category By Hour")
fig5=chart5.figure 
fig5.set_size_inches(20,6)
fig5.tight_layout(pad=2)
chart5.set_xlabel('Acorn Category by Hour')
chart5.set_ylabel('Electricity Usage, x 1,000,000 KWH')
fig5.savefig('NEW_'+block+' By Acorn Category By Hour.png',dpi=125)
'''

# create chart for final overall usage by Acorn Type
df6=pd.read_csv('Overall_Usage_By_Type.csv', names=['Type', 'Total_Usage'])
chart6=df6.plot(legend=False,x='Type', y='Total_Usage',kind='bar',title="Total Electricity Usage By Acorn Type")
fig6=chart6.figure 
fig6.set_size_inches(8,4)
fig6.tight_layout(pad=3)
chart6.set_xlabel('Acorn Type')
chart6.set_ylabel('Electricity Usage KWH')
fig6.savefig('Total Usage By Acorn Type.png',dpi=125)

# create chart for final overall usage by Acorn Category
df7=pd.read_csv('Overall_Usage_By_Category.csv', names=['Acorn Category', 'Total_Usage'])
df7.Total_Usage=df7.Total_Usage/1000000
chart7=df7.plot(legend=False,x='Acorn Category', y='Total_Usage',kind='bar',title="Total Electricity Usage By Acorn Category")
fig7=chart7.figure 
fig7.set_size_inches(6,5)
fig7.tight_layout(pad=4)
chart7.set_xlabel('Acorn Category')
chart7.set_ylabel('Electricity Usage, x 1,000,000 KWH')
fig7.savefig('Total Usage By Acorn Category.png',dpi=125)


# API weather data from darksky.net for UK locations

