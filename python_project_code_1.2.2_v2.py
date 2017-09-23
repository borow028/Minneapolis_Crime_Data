from pandas import Series, DataFrame
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

#CrimeDataDayLevel
data = pd.read_csv('CrimeDataDayLevel.csv',parse_dates=['BeginDate','ReportedDate','EnteredDate','lastchanged','LastUpdateDate'])

data['CrimeDate'] = data['BeginDate'].dt.date
data['Year'] = data['BeginDate'].dt.year
data['Year'] = data['Year'].astype('str')
data['Year-Month'] = pd.PeriodIndex(data['BeginDate'],freq='M') #to represent year-month of the crime
data['Month'] = data['BeginDate'].dt.month

data['Weekday'] = data['BeginDate'].dt.weekday   # 0 is Monday
data['Hour'] = data['BeginDate'].dt.hour

#categorizing offence types
segment_data = pd.read_csv('Segment_data.csv')
data = pd.merge(data, segment_data, on = "Offense")

#merging sectors
precinct_data = pd.read_csv('Precinct_Data.csv')
data = pd.merge(data,precinct_data, on = "Neighborhood")

#creating a dataset with data till 2015
data2 = data[data['Year'] != '2016']

#########################################################################################################################


#1.2.2 - Variation in Number of Crimes by Precinct and Crime Type  --- HEAT MAP

dataA = data2[['Year','Segment','CCN','New_precinct']]
dataA['Precinct-Year'] = dataA['New_precinct'].map(str) +' '+ dataA['Year']
crimeByPrecinctYearBySegment = dataA.groupby(['Precinct-Year','Segment']).size().unstack()
crimeByPrecinctYearBySegment = crimeByPrecinctYearBySegment.fillna(0)

column_labels = crimeByPrecinctYearBySegment.index
row_labels = crimeByPrecinctYearBySegment.columns

fig, ax = plt.subplots()
norm2= mpl.colors.Normalize(vmin=0.0, vmax=1000.0)
heatmap = ax.pcolormesh(crimeByPrecinctYearBySegment, cmap='Greens',alpha=1,norm=norm2,edgecolors='k')
ax.set_xticks(np.arange(crimeByPrecinctYearBySegment.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(crimeByPrecinctYearBySegment.shape[0])+0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels,minor=False)
fig.colorbar(heatmap,extend='max')
fig.show()

fig, ax = plt.subplots()
norm2= mpl.colors.Normalize(vmin=0.0, vmax=1250.0)
heatmap = ax.pcolormesh(crimeByPrecinctYearBySegment, cmap='Greens',alpha=1,norm=norm2,edgecolors='k')
ax.set_xticks(np.arange(crimeByPrecinctYearBySegment.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(crimeByPrecinctYearBySegment.shape[0])+0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels,minor=False)
fig.colorbar(heatmap,extend='max')
fig.show()

#1.2.2 - Variation in Number of Crimes by Neighborhood by Crime Type  --- HEAT MAP

dataSegmentNeighborhoodCNN = data2[['Neighborhood','New_precinct','Segment','CCN','Year']]
dataSegmentNeighborhoodCNN['Precinct-Neighborhood'] = dataSegmentNeighborhoodCNN['New_precinct'].map(str) +' '+ dataSegmentNeighborhoodCNN['Neighborhood']
crimeBySegmentByNeighborhood = dataSegmentNeighborhoodCNN.groupby(['Precinct-Neighborhood','Segment']).size().unstack()
crimeBySegmentByNeighborhood = crimeBySegmentByNeighborhood.fillna(0)
column_labels =  crimeBySegmentByNeighborhood.index #Appear as rows in the plot
row_labels = crimeBySegmentByNeighborhood.columns

fig, ax = plt.subplots()
norm2= mpl.colors.Normalize(vmin=0.0, vmax=400.0)
heatmap = ax.pcolormesh(crimeBySegmentByNeighborhood, cmap='Blues',alpha=1,edgecolors='k',norm=norm2) #RdBu_r #Reds
ax.set_xticks(np.arange(crimeBySegmentByNeighborhood.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(crimeBySegmentByNeighborhood.shape[0])+0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels, minor=False)
fig.colorbar(heatmap,extend='max')
fig.show()