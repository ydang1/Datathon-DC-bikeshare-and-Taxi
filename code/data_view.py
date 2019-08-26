# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 19:25:02 2019

@author: YIFAN DANG
"""
import os
import pandas as pd
import numpy as np
import gc
import matplotlib.pyplot as plt
from scipy import stats
gc.collect()

os.chdir('C:/Users/YIFAN DANG/Desktop/Datathon')

bikeshare=pd.read_csv('bikeshare.csv')
DCTaxi=pd.read_csv('DCTaxi.csv',nrows=10000)

bikeshare.info()
summary_bike=bikeshare.describe()
DCTaxi.info()
summary_taxi=DCTaxi.describe()

bikenumber_histogram=plt.hist(bikeshare['Duration'],bins=50
                              ,density=True)

#check unique Bikenumber
len(bikeshare['Duration'].unique())

#check End station number
len(bikeshare['End station number'].unique())

#check Start station number
len(bikeshare['Start station number'].unique())

#check Member type
len(bikeshare['Member type'].unique())

#duration check
maxduration=bikeshare[bikeshare['Duration']==86394]
minduration=bikeshare[bikeshare['Duration']==60]
len(minduration['Bike number'].unique())
len(minduration[minduration['Member type']=='Member'])
len(minduration[minduration['Member type']=='Casual'])

same1=bikeshare[(bikeshare['Start station number']==31266)&(bikeshare['End station number']==31281)]
same2=bikeshare[(bikeshare['Start station number']==31281)&(bikeshare['End station number']==31266)]
same=pd.concat([same1,same2],axis=0)
same=same.groupby('Bike number').filter(lambda x: len(x)>1)
same=same.sort_values(by=['Bike number'])
same_describe=same.describe()
same.to_csv('round_trip.csv')

#taxi duration check
max_row=DCTaxi['Duration'].idxmax()
taxi_maxduration=DCTaxi.loc[[max_row]]

###remove outliers###
mean_duration=np.mean(DCTaxi['Duration'])
std_duration=np.std(DCTaxi['Duration'])
mean_totalamount=np.mean(DCTaxi['TotalAmount'])
std_totalamount=np.std(DCTaxi['TotalAmount'])
mean_mileage=np.mean(DCTaxi['Mileage'])
std_mileage=np.std(DCTaxi['Mileage'])

#def outliers(data):
#    new_data=pd.DataFrame()
#    for i in (7,24,25):
#        mean=np.mean(data.iloc[:,i])
#        std=np.std(data.iloc[:,i])
#        for j in range(len(DCTaxi)):
#            if data.iat[j,i]<=(mean-3*std) or data.iat[j,i]>=(mean+3*std):
#                new_data.append(data.loc[[j]])
#    return new_data
#outliers(DCTaxi)

DCTaxi=pd.read_csv('DCtaxi_selected.csv')
#sample_DCTaxi=DCTaxi.iloc[:10000,:]
#sample_DCTaxi.to_csv('sample_DCTaxi.csv')
DCTaxi_stats=DCTaxi.describe()
DCTaxi=DCTaxi[(DCTaxi['Duration']>0)&(DCTaxi['milage']>0)&(DCTaxi['TotalAMount']>0)]
DCTaxi['milage']=DCTaxi['milage'][(np.abs(stats.zscore(DCTaxi['milage']))<3)]
DCTaxi['Duration']=DCTaxi['Duration'][(np.abs(stats.zscore(DCTaxi['Duration']))<3)]
DCTaxi['TotalAMount']=DCTaxi['TotalAMount'][(np.abs(stats.zscore(DCTaxi['TotalAMount']))<3)]

for i in range(len(DCTaxi)):
    if DCTaxi['Duration'][i]>120:
        DCTaxi['Duration'][i]=DCTaxi['Duration'][i]/60
return DCTaxi

DCTaxi['Duration']=DCTaxi[(DCTaxi['Duration']
DCTaxi['milage per minute']=DCTaxi['milage']/DCTaxi['Duration']
DCTaxi_stats=DCTaxi.describe()
DCTaxi.to_csv('DCtaxi.csv')

capitalbike=pd.read_csv('capitalbikeshare_selected.csv')
capitalbike=capitalbike[capitalbike['Duration']>0]
capitalbike['Duration']=capitalbike['Duration'][(np.abs(stats.zscore(capitalbike['Duration']))<3)]
capitalbike['Duration in Minutes']=capitalbike['Duration']/60
capitalbike_stats=capitalbike.describe()  
capitalbike.to_csv('capitalbike.csv')

##reverse geocoding
zip_code=pd.read_csv('US Zip Codes from 2013 Government Data')

Startzipcode=[]
for i in range(len(capitalbike)):
    for j in range(len(zip_code)):
        if (capitalbike.iloc[i,1]==zip_code.iloc[j,1])and(capitalbike.iloc[i,2]==zip_code.iloc[j,2]):
            Startzipcode.append(zip_code[j,0])
return Startzipcode

capitalbike=pd.read_csv('capitalbikes.csv')  
capitalbike['Duration']=capitalbike['Duration'][(np.abs(stats.zscore(capitalbike['Duration']))<3)]
capitalbike['Duration per minute']=capitalbike['Duration']/60 
capitalbike_stats=capitalbike.describe()
capitalbike.to_csv('capitalbike.csv') 
        













        



