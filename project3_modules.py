import pandas as pd
import numpy as np
import matplotlib
import datetime
import pickle
import sqlite3
from matplotlib import pyplot as plt

# %matplotlib inline  # this code is only to plot inline in Jupyter Notebook

#read, clean and format data
def clean_format_csv(filename):
    df=pd.read_csv(filename, na_values=[' ','Null','null','N/A','na','',float('inf'), float('-inf'), np.inf, -np.inf])      
    print (filename, df.shape)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True) 
    df.DateTime=pd.to_datetime(df.DateTime) #convert DateTime column from str to DateTime dtype
    df['Year']=df.DateTime.dt.year #add 'Year' column based on Year valud in DateTime col
    df['Month']=df.DateTime.dt.month #add 'Month' column based on Month value in DateTime col
    df['Day_of_Week (Mon=0 .. Sun=6)']=df.DateTime.dt.dayofweek  #add 'Date_of_Week [Mon=0 .. Sun=6]' column based on dayofweek value in DateTime col
    df['Hour']=df.DateTime.dt.hour #add 'Hour' column based on Hour valud in DateTime col
    df.to_csv(filename, sep=',') # overwrite data file with cleaned up version with added columns
    print (filename, df.shape)

# merge dfs 
def merge_blockdata_and_type(blockfilename,typefilename):
    df_merged=pd.DataFrame()
    df1=pd.read_csv(blockfilename)
    df2=pd.read_csv(typefilename)
    print (df1.head())
    print (df2.head())
    df_merged=pd.merge(df1,df2,how='left',on='LCLid')
    print (df_merged.tail())
    print type(df_merged)
    print df_merged.dtypes
    return df_merged  # failed to return as pd.DataFrame type  #why?

# analyze and visualize data one block at a time and merge dfs 
# enter one filename at a time and run this scripts
def analyze_visualize (filename):
    block=filename
    df1=pd.read_csv(block)
    df2=pd.read_csv('household_shortfile.csv', na_values=['ACORN-U','ACORN-']) # to drop incomplete 
    df2.dropna(inplace=True) 
    df_merged=pd.merge(df1,df2,how='left',on='LCLid')
    df_merged.dropna(inplace=True)
    # create plots
    # chart1    
    s1=df_merged.groupby('Acorn_grouped',as_index=True)['KWH/hh (per half hour) '].sum()
    chart1=s1.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Category")
    fig1=chart1.figure 
    fig1.set_size_inches(6,4)
    fig1.tight_layout(pad=2)
    chart1.set_xlabel('Acorn Category')
    chart1.set_ylabel('Electricity Usage KWH')
    fig1.savefig(block+' By Acorn Category.png',dpi=125)
    # chart2
    s2=df_merged.groupby('Acorn',as_index=True)['KWH/hh (per half hour) '].sum()
    chart2=s2.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Type")
    fig2=chart2.figure 
    fig2.set_size_inches(6,4)
    fig2.tight_layout(pad=3)
    chart2.set_xlabel('Acorn Type')
    chart2.set_ylabel('Electricity Usage KWH')
    fig2.savefig(block+' By Acorn Type.png',dpi=125)
    # char3    
    s3=df_merged.groupby(['Acorn_grouped','Month'])['KWH/hh (per half hour) '].sum()
    chart3=s3.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Category By Month")
    fig3=chart3.figure 
    fig3.set_size_inches(10,6)
    fig3.tight_layout(pad=3)
    chart3.set_xlabel('Acorn Category')
    chart3.set_ylabel('Electricity Usage KWH')
    fig3.savefig(block+' By Acorn Category By Month.png',dpi=125)
    # chart4
    s4=df_merged.groupby(['Acorn_grouped','Year'])['KWH/hh (per half hour) '].sum()
    chart4=s4.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Category By Year")
    fig4=chart4.figure 
    fig4.set_size_inches(8,4)
    fig4.tight_layout(pad=3)
    chart4.set_xlabel('Acorn Category')
    chart4.set_ylabel('Electricity Usage KWH')
    fig4.savefig(block+' By Acorn Category By Year.png',dpi=125)
    # chart5
    s5=df_merged.groupby(['Acorn_grouped','Hour'])['KWH/hh (per half hour) '].sum()
    chart5=s5.plot(kind='bar',title=block+"    Total Electricity Usage By Acorn Category By Hour")
    fig5=chart5.figure 
    fig5.set_size_inches(20,4)
    fig5.tight_layout(pad=3)
    chart5.set_xlabel('Acorn Category')
    chart5.set_ylabel('Electricity Usage KWH')
    fig5.savefig(block+' By Acorn Category By Hour.png',dpi=125)

