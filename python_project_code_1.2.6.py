#Predictive model on number of Theft of Vechicle Crimes

from pandas import DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf


#CrimeDataDayLevel
data = pd.read_csv('CrimeDataDayLevel.csv',parse_dates=['BeginDate'])

data['CrimeDate'] = data['BeginDate'].dt.date
data['Year'] = data['BeginDate'].dt.year
data['Year'] = data['Year'].astype('str')
data['Year-Month'] = pd.PeriodIndex(data['BeginDate'],freq='M')
data['Date'] = pd.PeriodIndex(data['BeginDate'],freq='D') 
data['Month'] = data['BeginDate'].dt.month
data['Day'] = data['BeginDate'].dt.day

segment_data = pd.read_csv('Segment_data.csv')
data = pd.merge(data, segment_data, on = "Offense")

data1 = data[data['Segment'] == 'Theft of vehicle']
data1 = data1.groupby(['Year-Month']).size()
data1 = DataFrame(data1)
data1.reset_index(['Year-Month', 'crimes'], drop=False, inplace=True)
data1.columns = ['Year-Month','Actual_Crimes']
data1 = data1.set_index(['Year-Month'])
data1['Month'] = data1.index.month
data1['Trend'] = range(1, len(data1) + 1)
data1['Lag_1_Crimes'] = data1['Actual_Crimes'].shift(periods = 1)

data2 = data1[data1.Trend != 1]
data2['Month_cat'] = data2['Month'].astype("category")

#predictive model
mod = smf.ols("Actual_Crimes ~ Trend + np.multiply(Trend,Trend) + Month_cat + Lag_1_Crimes", data2).fit()
print(mod.summary())

data2['Actual_Crimes'].plot(kind='line')
fitted_values = mod.fittedvalues 
plt.plot(fitted_values, color='red')
plt.title('Actual vs predicted #crime')
plt.ylabel('Number of Crimes')
plt.xlabel('Year')
plt.show()
