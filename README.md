# Project Descripton (sponsored by Smith Analytics Consortium members: Deloitte, KPMG, MERKLE)
In 2019, city-goers have access to a range of transportation modes, whereas 20 years ago options were limited. Transportation companies that thrived when consumers were limited are now forced to rethink their approach to their current market share of city travelers. This is a 4-person team projects that uses problem sloving, analytics, and data visualization skills to analyze the impact of intermediate transportation trends within the DC Metro area as it relates to Capital Bikeshare and DC Taxis, and present recommendataions for impacted businesses(i.e, taxi companies) to consider in their effort to regain their market share, 

# DataSet
1. Capital BikeShare(2016 - 2017): Where do Capital Bikeshare riders go?  When do they ride? How far do they go? Which stations are most popular?  What days of the week are most rides taken on? All of this data and more has been collected since the company started in 2010.
![](presentation/bikeshare%20columns.png)

2. DC For- Hire(Taxi): The DC Office of the Chief Technology Officer has shared samples of DC Taxicab trip data by month and year. Pick up and drop off locations with times rounded to the nearest hour. Data such as fare total, payment type, miles trveled and pick up/drop off times are included. 
![](presentation/taxi%20columns.png)

# Prerequistes
tools:
- Tableau(Visualization): https://www.tableau.com/products/desktop/download
- Python(Data Analysis): https://www.anaconda.com/distribution/
- Google Cloud Platform (GCP) Big Query(Data Analysis): https://console.cloud.google.com/bigquery?project=umd-sac-datathon
- GCP Cloud Storage(Data Storage): https://console.cloud.google.com/storage/browser/umdsac-datathon-rawdata/?prefix=cleaned_datasets&project=umd-sac-datathon

# Running the tests
## 1. Based on same zipcode area, used Big Query to select the key features for both Bikeshare and taxis data. Exploring the data and removed missing value and outliers. 

```
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

```

Bikeshare (Select the same zipcode for OriginZip and DestinationZip):

|Bike_number |StartLatitude |StartLongitude |EndLatitude |EndLogitude |OriginZip |DestinationZip |Duration |Duration per minute|
|------------|--------------|---------------|------------|------------|----------|---------------|---------|-------------------|
|W20870|	               38.9086|	   -77.0323|	   38.9086|	 -77.0323|	    20005|	      20005|	    904.0|	15.066666666666666|
|W22962|	               38.9176|  	 -77.0321|	   38.9176|	 -77.0321|	    20010|	      20010|	     80.0|	1.3333333333333333|

sample_DCTaxi:

|externalID |OriginZip |DestinationZip |TotalAMount	milage |Duration|
|-----------|----------|---------------|-------------------|--------|
|70300_26NQE2DC |20045 |20008 |15.38 |4.53 |906|
|52753_26NFPSK9 |	20002 |20001 |8.9 |1.25 |546|




## 2. Data visualization (plot in Tableau)
![](data%20visualization/bike%20start%20station.png)

![](data%20visualization/bike%20end%20station.png)

![](data%20visualization/bike%20round%20trip%20stations.png)

![](data%20visualization/bike%20round%20trip%20stations%20neighborhood.png)

taxi starts and ends station
![](data%20visualization/taxi%20station.png)

DC bike Density
![](data%20visualization/DC%20bike%20density.png)

DC taxi density
![](data%20visualization/DC%20taxi%20density.png)

Daily bikeshare and taxis change
![](data%20visualization/Picture1.png)

seasonal bikeshare and texis change
![](data%20visualization/Picture2.png)

# Conclusion & interesting findings
1. Taxi Company should have potential growth by regaining the market in zipcode areas 20009 and 20003, whereas decrease the taxi distribution in downtown DC areas such as zipcode 20024 because it has a high density of bikeshares.

2. There are only two bikeshare stations which bike riders did round trip.(start from one and end on the other and vice versa). As we open the google map and find out the neighborhood around these two bikeshare station, we find there are a shopping mall, recreation center and school around this area. 

3. The daily bikeshare numbers start increases from 5:00 A.M. and reach the peak point near 8 A.M., then suddenly decrease, And start increase again from 3:00 P.M. and reach the peak point near 5:00 P.M., then drop again. It could be that there a lot of people take advantage of using bikeshare right before the rush hour starts to avoid the traffics. 

4. The seasonal graph shows that during the winter, people like both bikeshare and taxi, it could be biking in winter is a good outdoor exercises for most of the people.

## Future Imporvement
- used multiple random subsets of data to do the distribution on the map to make comparison. It might save more time then plot the whole dataset all together in tableau.
- Doulbe Check the data set, make sure there are no abnormal value apprears when ploting the grapg, some information like the duration within the same zipcode area could be too large to be trusted.
- Consider more features, conduct a predictive model if necessary for future analysis.

# Contribution
- Assigned a new team and help team members understand the task and the work process from a high level.
- Used big query to select data contained necessary informations.
- used Tableau to visualze the bike and taxi spatial distributions on geographic map.
- Used Python to explore and manipulate the data for team members to conduct daily and seasonal visualization
- Lead the team to work on the presentation slides, voiceover and support team with any necessary documents. 



