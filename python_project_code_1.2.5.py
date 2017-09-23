#Neighborhood Scoring

import numpy as np
import pandas as pd
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

#loading weekday names
week_data = pd.read_csv('Week_data.csv')
data = pd.merge(data,week_data, on = "Weekday")

#categorizing parts of a day
time_data = pd.read_csv('Time_data.csv')
data = pd.merge(data,time_data, on = "Hour")

#loading seasons of a year
season_data = pd.read_csv('Seasons_data.csv')
data = pd.merge(data,season_data, on = "Month")

data2 = data[data['Year'] != '2016']

#Neighborhood Scoring 
#########################################################################################################################

print '\nFind below the weightage associated with crime types for the Neighbourhood score :'
print 'Homicide - 0.2'
print 'Rape - 0.2'
print 'Domestic assault - 0.15'
print 'Theft of vehicle - 0.1'
print 'Theft of place/property - 0.1'
print 'Theft of person - 0.1'
print 'Other theft - 0.1'
print 'Other crimes - 0.05'

print '\nEnter the weightages :'
homicide = float(raw_input('Enter weightage for Homicide (0.2) :' ))
rape = float(raw_input('Enter weightage for Rape (0.2) :' ))
dom_ass = float(raw_input('Enter weightage for Domestic assault (0.15) :' ))
theft_veh = float(raw_input('Enter weightage for Theft of vehicle (0.1) :' ))
theft_place = float(raw_input('Enter weightage for Theft of place/property (0.1) :' ))
theft_per = float(raw_input('Enter weightage for Theft of person (0.1) :' ))
other_theft = float(raw_input('Enter weightage for Other theft (0.1) :' ))
other_crime = float(raw_input('Enter weightage for Other crimes (0.05) :' ))

NHdata1 = data2[['Neighborhood','Segment','CCN']]
NHdata = NHdata1.groupby(['Neighborhood','Segment']).size().unstack()
NHdata = NHdata.fillna(0)

max_value = NHdata['Domestic assault'].max()
min_value = NHdata['Domestic assault'].min()
range_value = max_value - min_value
NHdata['Domestic assault'] = (NHdata['Domestic assault'] - min_value)/range_value

max_value = NHdata['Rape'].max()
min_value = NHdata['Rape'].min()
range_value = max_value - min_value
NHdata['Rape'] = (NHdata['Rape'] - min_value + 0.1)/range_value

max_value = NHdata['Homicide'].max()
min_value = NHdata['Homicide'].min()
range_value = max_value - min_value
NHdata['Homicide'] = (NHdata['Homicide'] - min_value + 0.1)/range_value

max_value = NHdata['Theft of vehicle'].max()
min_value = NHdata['Theft of vehicle'].min()
range_value = max_value - min_value
NHdata['Theft of vehicle'] = (NHdata['Theft of vehicle'] - min_value + 0.1)/range_value

max_value = NHdata['Theft of person'].max()
min_value = NHdata['Theft of person'].min()
range_value = max_value - min_value
NHdata['Theft of person'] = (NHdata['Theft of person'] - min_value + 0.1)/range_value

max_value = NHdata['Theft of place/property'].max()
min_value = NHdata['Theft of place/property'].min()
range_value = max_value - min_value
NHdata['Theft of place/property'] = (NHdata['Theft of place/property'] - min_value + 0.1)/range_value

max_value = NHdata['Other theft'].max()
min_value = NHdata['Other theft'].min()
range_value = max_value - min_value
NHdata['Other theft'] = (NHdata['Other theft'] - min_value + 0.1)/range_value

max_value = NHdata['Other crimes'].max()
min_value = NHdata['Other crimes'].min()
range_value = max_value - min_value
NHdata['Other crimes'] = (NHdata['Other crimes'] - min_value + 0.1)/range_value


NHdata['NH_base_score'] = (NHdata['Domestic assault'] * 0.15 +   NHdata['Rape'] * 0.2 +   NHdata['Homicide'] * 0.2 +   NHdata['Theft of vehicle'] * 0.1 +   NHdata['Theft of person'] * 0.1 +   NHdata['Theft of place/property'] * 0.1 +   NHdata['Other theft'] * 0.1 +   NHdata['Other crimes'] * 0.05)/8
NHdata['NH_wt_score'] = (NHdata['Domestic assault'] * dom_ass +   NHdata['Rape'] * rape +   NHdata['Homicide'] * homicide  +   NHdata['Theft of vehicle'] * theft_veh +   NHdata['Theft of person'] * theft_per  +   NHdata['Theft of place/property'] * theft_place +   NHdata['Other theft'] * other_theft +   NHdata['Other crimes'] * other_crime)/8

NHdataOriginalScore = NHdata[['NH_base_score']]
NHdataOriginalScore = NHdataOriginalScore.sort('NH_base_score').head(10)
print NHdataOriginalScore

NHdataWtScore = NHdata[['NH_wt_score']]
NHdataWtScore = NHdataWtScore.sort('NH_wt_score').head(10)
print NHdataWtScore

NHdataOriginalScore1 = NHdata[['NH_base_score']]
NHdataOriginalScore1 = NHdataOriginalScore1.sort('NH_base_score').tail(10)
print NHdataOriginalScore1

NHdataWtScore1 = NHdata[['NH_wt_score']]
NHdataWtScore1 = NHdataWtScore1.sort('NH_wt_score').tail(10)
print NHdataWtScore1

NHdataOriginalScore.plot(kind='barh', title = "Top 10 safest neighborhoods by NH_base_score")
NHdataWtScore.plot(kind='barh', title = "Top 10 safest neighborhoods by NH_wt_score")
NHdataOriginalScore1.plot(kind='barh', title = "Top 10 unsafe neighborhoods by NH_base_score") 
NHdataWtScore1.plot(kind='barh', title = "Top 10 unsafe neighborhoods by NH_wt_score") 
plt.show()