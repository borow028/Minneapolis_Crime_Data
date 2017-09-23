import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


#CrimeDataDayLevel
data = pd.read_csv('CrimeDataDayLevel.csv',parse_dates=['BeginDate'])

data['CrimeDate'] = data['BeginDate'].dt.date
data['Year'] = data['BeginDate'].dt.year
data.round(0)
print data['Year'].head() 
data['Year'] = data['Year'].astype('str')
data['Year-Month'] = pd.PeriodIndex(data['BeginDate'],freq='M') #to represent year-month of the crime
data['Weekday'] = data['BeginDate'].dt.weekday   # 0 is Monday
data['Month'] = data['BeginDate'].dt.month
data['Precinct'] = data['Precinct'].astype('str')

#categorizing offence types
segment_data = pd.read_csv('Segment_data.csv')
data = pd.merge(data, segment_data, on = "Offense")

#loading weekday names
week_data = pd.read_csv('Week_data.csv')
data = pd.merge(data,week_data, on = "Weekday")

#loading seasons of a year
season_data = pd.read_csv('Seasons_data.csv')
data = pd.merge(data,season_data, on = "Month")

#creating a dataset with data till 2015
data2 = data[data['Year'] != '2016']

#########################################################################################################################
#Number of Crimes by Crime Type by Month -- AREA GRAPH

# Function to plot data grouped by Dates and Category
def plotTimeGroup(dfGroup, ncols=10, area=False, title=None):
    categoryCV = pd.DataFrame(columns=["Category", "CV"])
    rows = []

    for column in dfGroup.columns:
        col = dfGroup[column]
        # Only consider category, if there are enough samples
        if (col.sum() > 500):
            rows.append({'Category': column, 'CV': col.std() / col.mean()})

    categoryCV = pd.DataFrame(rows).sort_values(by="CV", ascending=0)
    #The graph with all categories is unreadable. Therefore, columns with a
    # high coefficient of variation are extracted:
    topCVCategories = categoryCV[:ncols]["Category"].tolist()
    f = plt.figure(figsize=(13,8))
    ax = f.gca()
    if area:
        dfGroup[topCVCategories].plot.area(ax=ax, title=title, colormap="jet")
    else:
        dfGroup[topCVCategories].plot(ax=ax, title=title, colormap="jet")
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=1, fontsize=11)
    
crimeBySegmentByMonth = data2.groupby(['Year-Month','Segment']).size().unstack()
plotTimeGroup(crimeBySegmentByMonth, title='Number of Crimes by Segment by Month', area=True)
plt.show()

#########################################################################################################################
#Variation in Number of Crimes by Neighborhood by Crime Type  --- HEAT MAP

dataSegmentNeighborhoodCNN = data[['Neighborhood','Segment','CCN','Year']]
crimeBySegmentByNeighborhood = dataSegmentNeighborhoodCNN.groupby(['Neighborhood','Segment']).size().unstack()
crimeBySegmentByNeighborhood = crimeBySegmentByNeighborhood.fillna(0)
column_labels =  crimeBySegmentByNeighborhood.index #Appear as rows in the plot
row_labels = crimeBySegmentByNeighborhood.columns

fig, ax = plt.subplots()
norm1= mpl.colors.SymLogNorm(linthresh=0.05, linscale=0.05,vmin=0.0, vmax=7500.0)
heatmap = ax.pcolormesh(crimeBySegmentByNeighborhood, cmap='Blues',alpha=1,edgecolors='k',norm=norm1) #RdBu_r #Reds
ax.set_xticks(np.arange(crimeBySegmentByNeighborhood.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(crimeBySegmentByNeighborhood.shape[0])+0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels, minor=False)
ax.set_ylabel('Precinct - Neighborhood')
ax.set_xlabel('Segment Type')
fig.colorbar(heatmap,extend='max')
fig.show()

#########################################################################################################################
##Variation in Number of Crimes by Precinct and Crime Type  --- HEAT MAP
dataA = data[['Year','Segment','CCN','Precinct']]

dataA['Precinct-Year'] = dataA['Precinct'].map(str) +' '+ dataA['Year']
crimeByPrecinctYearBySegment = dataA.groupby(['Precinct-Year','Segment']).size().unstack()
crimeByPrecinctYearBySegment = crimeByPrecinctYearBySegment.fillna(0)

column_labels =  crimeByPrecinctYearBySegment.index
row_labels = crimeByPrecinctYearBySegment.columns

fig, ax = plt.subplots()
norm2= mpl.colors.Normalize(vmin=0.0, vmax=2000.0)
heatmap = ax.pcolormesh(crimeByPrecinctYearBySegment, cmap='Greens',alpha=1,norm=norm2,edgecolors='k')

ax.set_xticks(np.arange(crimeByPrecinctYearBySegment.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(crimeByPrecinctYearBySegment.shape[0])+0.5, minor=False)

ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_ylabel('Precinct - Year')
ax.set_xlabel('Segment')
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels,minor=False)
fig.colorbar(heatmap,extend='max')
fig.show()

##########################################################################################################################
##Number of Crimes by Year by Weekday  -- LINE GRAPH

data2['Weekday-Year'] = data2.Wkday.str.cat(' '+data2.Year)
data2['Weekday-Year'] = data2['Weekday-Year'].astype('str')
crimeBySegmentByWeekday = data2.groupby(['Weekday-Year','Segment']).size().unstack()
crimeBySegmentByWeekday.plot(grid=True,title='Number of Crimes by Weekday and Crime Type')
plt.subplot()
ax.set_ylabel('Number of Crimes')
ax.set_xlabel('Weekday-Year')
xValues = crimeBySegmentByWeekday.index
plt.xticks( np.arange(42), xValues, rotation=45 )
plt.show()

#########################################################################################################################
#Number of Crimes by Year by Weekday  -- LINE GRAPH

data2['Season-Year'] = data2.Season.str.cat(' '+data2.Year)
data2['Season-Year'] = data2['Season-Year'].astype('str')
crimeBySegmentBySeason = data2.groupby(['Season-Year','Segment']).size().unstack()
crimeBySegmentBySeason.plot(grid=True,title='Number of Crimes by Season and Year')
ax.set_ylabel('Number of Crimes')
ax.set_xlabel('Season-Year')
xValues = crimeBySegmentBySeason.index
plt.xticks( np.arange(24), xValues, rotation=45 )
plt.show()

#########################################################################################################################
#Variation in number of Crimes by Season Year by CrimeType  -- HEAT MAP

dataSeasonYearSegment = data2[['Year','Segment','CCN','Season']]
dataSeasonYearSegment['Season-Year'] = dataSeasonYearSegment.Season.str.cat(' '+dataSeasonYearSegment.Year)
dataSeasonYearSegment = dataSeasonYearSegment.groupby(['Season-Year','Segment']).size().unstack()
dataSeasonYearSegment = dataSeasonYearSegment.fillna(0)

column_labels =  dataSeasonYearSegment.columns
row_labels = dataSeasonYearSegment.index

column_labels =  dataSeasonYearSegment.index#Appear as rows in the plot
row_labels = dataSeasonYearSegment.columns

fig, ax = plt.subplots()
norm2= mpl.colors.Normalize(vmin=0.0, vmax=2000.0)
heatmap = ax.pcolormesh(dataSeasonYearSegment, cmap='cool',alpha=1,norm=norm2,edgecolors='k')

ax.set_xticks(np.arange(dataSeasonYearSegment.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(dataSeasonYearSegment.shape[0])+0.5, minor=False)

ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_ylabel('Number of Crimes')
ax.set_xlabel('Season-Year')
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels, minor=False)
fig.colorbar(heatmap,extend='max')
fig.show()