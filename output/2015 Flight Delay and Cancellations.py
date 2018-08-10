
# coding: utf-8

# # 2015 Flight Delay and Cancellations

# ## Setup and Imports

# In[1]:


import datetime, warnings, scipy 
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
#from mpl_toolkits.basemap import Basemap
from collections import OrderedDict
from matplotlib.colors import Normalize, LinearSegmentedColormap, PowerNorm

get_ipython().run_line_magic('matplotlib', 'inline')
warnings.filterwarnings("ignore")

airlines = pd.read_csv('../data/airlines.csv')
airports= pd.read_csv('../data/airports.csv')
flights = pd.read_csv('../data/flights.csv', low_memory=False)


# In[2]:


plt.style.use('fivethirtyeight')
plt.rcParams["patch.force_edgecolor"] = True
mpl.rc('patch', edgecolor = 'dimgray', linewidth=1)
pd.set_option('max_rows', 10)


# ## Correlation between route distance and flight delays.

# In[6]:


print ('MAX DELAY: '+str(np.amax(flights['DEPARTURE_DELAY'])))
print ('MIN DELAY: '+str(np.amin(flights['DEPARTURE_DELAY'])))
print ('MEAN DELAY: '+str(np.mean(flights['DEPARTURE_DELAY'])))
print ('STD DEV of DELAY: '+str(np.std(flights['DEPARTURE_DELAY'])))
print ('VARIANCE OF DELAY: '+str(np.var(flights['DEPARTURE_DELAY'])))


# In[13]:


plt.figure(figsize=(20,10))
plt.plot(flights['DISTANCE'], flights['DEPARTURE_DELAY'], 'o', color='black') #This needs to be total delay not just departure delay
plt.xlabel("Distance")
plt.ylabel("Departure delay");
plt.show()


# In[87]:


print("Numpy Correlate: "+str(np.correlate(flights['DISTANCE'], flights['DEPARTURE_DELAY'])))
print("Numpy Correlation Coefficient: "+str(np.corrcoef(flights['DISTANCE'], flights['DEPARTURE_DELAY'])))


# Based on the distribution of the plot of Distance and Departure Delay and the `nan` calculated correlation and correlation coefficient by numpy there does not appear to be any correlation between Distance and Departure Delay. 

# ## Which airports are part of the most delayed flights (either source or destination)?

# In[85]:


filtered_orig = flights[['ORIGIN_AIRPORT', 'DEPARTURE_DELAY']].rename(index=str, columns={"ORIGIN_AIRPORT": "IATA_CODE"})

delayed_orig_by_airport = filtered_orig.loc[ filtered_orig['DEPARTURE_DELAY'] > 0.0 ].groupby(['IATA_CODE'])
delayed_orig_mean = delayed_orig_by_airport.mean().rename(index=str, columns={"DEPARTURE_DELAY": "ORIGIN_DEPARTURE_DELAY_AVG"})
delayed_orig_count = delayed_orig_by_airport.size().reset_index(name='ORIGIN_DELAY_COUNT').sort_values(by=['ORIGIN_DELAY_COUNT'], ascending=False)
delayed_orig_stats_by_airport = pd.merge(delayed_orig_count, delayed_orig_mean, on='IATA_CODE')


filtered_dest = flights[['DESTINATION_AIRPORT', 'DEPARTURE_DELAY']].rename(index=str, columns={"DESTINATION_AIRPORT": "IATA_CODE"})
filtered_dest = pd.merge(filtered_dest, airports, on='IATA_CODE')[['IATA_CODE', 'AIRPORT', 'DEPARTURE_DELAY' ]]

delayed_dest_by_airport = filtered_dest.loc[ filtered['DEPARTURE_DELAY'] > 0.0 ].groupby('IATA_CODE')
delayed_dest_mean = delayed_dest_by_airport.mean().rename(index=str, columns={"DEPARTURE_DELAY": "DESTINATION_DEPARTURE_DELAY_AVG"})
delayed_dest_count = delayed_orig_by_airport.size().reset_index(name='DESTINATION_DELAY_COUNT').sort_values(by=['DESTINATION_DELAY_COUNT'], ascending=False)
delayed_dest_stats_by_airport = pd.merge(delayed_dest_count, delayed_dest_mean, on='IATA_CODE')

result = pd.merge(delayed_orig_stats_by_airport, delayed_dest_stats_by_airport, on='IATA_CODE')
result = pd.merge(result, airports, on='IATA_CODE')[['IATA_CODE', 'AIRPORT', 'ORIGIN_DELAY_COUNT', 'ORIGIN_DEPARTURE_DELAY_AVG','DESTINATION_DELAY_COUNT', 'DESTINATION_DEPARTURE_DELAY_AVG' ]]
result['TOTAL_DELAY_COUNT'] = result['ORIGIN_DELAY_COUNT'] + result['DESTINATION_DELAY_COUNT']


# In[91]:


result_orig_delay_count = result.sort_values(by=['ORIGIN_DELAY_COUNT'], ascending=False)
result_orig_delay_count.head()


# In[92]:


result_dest_delay_count = result.sort_values(by=['DESTINATION_DELAY_COUNT'], ascending=False)
result_dest_delay_count.head()


# In[101]:


result_total_delay_count = result.sort_values(by=['TOTAL_DELAY_COUNT'], ascending=False)
result_total_delay_count.head()


# ### Analysis
# Interestingly the top 5 airports to be involved with delayed flights are the same across the board. ATL, ORD, DFW, DEN and LAX are numbers 1-5 in that order for number of delayed flights as the origin city, number of delayed flights as the destination city and total number of delayed flights involved as is illustrated by the three tables above.
# 
# **NOTE: this does not necessarily mean these airports should be avoided because after further analysis represented in the two tables below these airports have a relatively small average delay time. Therefore, you may delayed but it likely won't be a significant delay.

# In[87]:


result_avg_orig_delay = result.sort_values(by=['ORIGIN_DEPARTURE_DELAY_AVG'], ascending=False)
result_avg_orig_delay


# In[88]:


result_avg_dest_delay = result.sort_values(by=['DESTINATION_DEPARTURE_DELAY_AVG'], ascending=False)
result_avg_dest_delay


# ## Which airline should you fly on to avoid significant delays?

# In[44]:


filtered = flights[['AIRLINE', 'DEPARTURE_DELAY']].rename(index=str, columns={"AIRLINE": "IATA_CODE"})

delayed_by_airline = filtered.loc[ filtered['DEPARTURE_DELAY'] > 0.0 ].groupby(['IATA_CODE'])
delayed_mean = delayed_by_airline.mean().rename(index=str, columns={"DEPARTURE_DELAY": "DEPARTURE_DELAY_AVG"}).sort_values(by=['DEPARTURE_DELAY_AVG'])

result = pd.merge(delayed_mean, airlines, on='IATA_CODE')[['IATA_CODE', 'AIRLINE', 'DEPARTURE_DELAY_AVG']]
result


# As shown in the table above Frontier Airlines has the highest average delay time across the whole year, with Spirit Airlines as a close second. This makes sense as they operate in almost exclusively the "budget airline" niche. On the other side of the spectrum are high quality, highly regional airlines such as Alaska Airlines and Hawaiian Airlines as the lowest average departure times. 

# In[47]:


filtered = flights[['AIRLINE', 'MONTH', 'DEPARTURE_DELAY']].rename(index=str, columns={"AIRLINE": "IATA_CODE"})
filtered = pd.merge(filtered, airlines, on='IATA_CODE')

delayed_by_airline_by_month = filtered.loc[ filtered['DEPARTURE_DELAY'] > 0.0 ].groupby(['IATA_CODE', 'AIRLINE', 'MONTH'])
delayed_mean = delayed_by_airline_by_month.mean().rename(index=str, columns={"DEPARTURE_DELAY": "DEPARTURE_DELAY_AVG"}).sort_values(by=['DEPARTURE_DELAY_AVG'])
pd.set_option('max_rows', 24)
delayed_mean


# However, upon closer analysis it's clear that the airline to avoid isn't so cut and dry. Spirit Airline actually has the highest monthly delay average in June. Frontier still takes 4 of the top 6 spots with the holiday season (12-2) and the peak vacation season June (6). On the other side the answer for which airline to fly if you want to avoid significant delays is clear. Hawaiian Airlines takes the top 11 spots unanimously. 

# ## Interesting Observations

# In my initial inspection of the dataset I noticed that DEPARTURE_DELAY often had negative values representing that the flight actually took off ahead of schedule. From that data we can see that not only does Alaska Airlines have one of the lowest average delays but when they are ahead of schedule they leave the furthest ahead. More interesting though is that Frontier and Spirit, the two airlines with the worst average delays, actually do great on average when they are ahead of schedule. However, I think one of the most important aspects to air travel is consistency. We can see that Southwest and Delta have some of the lowest average delays and smallest ahead of time meaning they are more consistent and precise with their timing.

# In[55]:


#average time ahead of schedule
filtered = flights[['AIRLINE', 'DEPARTURE_DELAY']].rename(index=str, columns={"AIRLINE": "IATA_CODE"})
filtered = pd.merge(filtered, airlines, on='IATA_CODE')

delayed_by_airline_by_month = filtered.loc[ filtered['DEPARTURE_DELAY'] < 0.0 ].groupby(['IATA_CODE', 'AIRLINE'])
delayed_mean = delayed_by_airline_by_month.mean().rename(index=str, columns={"DEPARTURE_DELAY": "DEPARTURE_AHEAD_AVG"}).sort_values(by=['DEPARTURE_AHEAD_AVG'])
result = pd.merge(delayed_mean, airlines, on='IATA_CODE')[['IATA_CODE', 'AIRLINE', 'DEPARTURE_AHEAD_AVG']]
pd.set_option('max_rows', 24)
result


# Even worse than a delayed flight is a cacnelled flight. Thankfully it happens a relatively small amount of time, only 1.544% of flights.

# In[54]:


number_of_delayed = flights["DEPARTURE_DELAY"].apply(lambda s: 1 if s>0 else 0);
print("Percentage of cancelled flights: "+str((sum(flights["CANCELLED"])*1.0/len(flights))*100)+"%")
print("Percentage of delayed flights: "+str((sum(number_of_delayed)*1.0/len(flights))*100)+"%")


# Sometimes cancellations are unavoidable for the airline and sometimes it is the airlines fault. Here I've categorized  the cancellation reasons into unavoidable (Weather, the NAS or security) and avoidable (carrier). We can see that the vast majority of cancellations come due to weather which makes sense. Bad weather is a big safety concern and it makes more sense to ground flights in those situations. On the other side a very low number of flights are cancelled due to security concerns which is good. Hopefully that means TSA screening and other preventative measures are working as intended.

# In[19]:


#number of unavoidable cancellations
cancellation_reasons = flights.rename(index=str, columns={"AIRLINE": "IATA_CODE"})[["CANCELLED","IATA_CODE","CANCELLATION_REASON"]]
unavoidable_cancellation_reasons = cancellation_reasons.loc[cancellation_reasons["CANCELLATION_REASON"].isin(['B','C', 'D'])].groupby(['IATA_CODE', 'CANCELLATION_REASON']).sum().reset_index()

unavoidable_cancellation_reasons = pd.merge(unavoidable_cancellation_reasons, airlines, on='IATA_CODE')
print("B - Weather; C - National Air System; D - Security")
pd.set_option('max_rows', 50)
unavoidable_cancellation_reasons[["IATA_CODE", "AIRLINE", "CANCELLATION_REASON", "CANCELLED"]].sort_values(by=['CANCELLED'],ascending=[False])


# Then there are the avoidable cancellations caused by the carrier. These are the more frustrating cancellations where on a beautiful sunny day, with barely anyone in the airport your flight might be cancelled leaving you stranded. Surprisingly the budget airlines did pretty well here. Southwest, however, was by far the worst for carrier cancellations with almost double the amount of the next highest. Lastly, Hawaiian Airlines continues to consistently perform in the top 3.

# In[18]:


#Worst airline for avoidable cancelations
cancellation_reasons = flights.rename(index=str, columns={"AIRLINE": "IATA_CODE"})[["CANCELLED","IATA_CODE","CANCELLATION_REASON"]]
avoidable_cancellation_reasons = cancellation_reasons.loc[cancellation_reasons["CANCELLATION_REASON"].isin(['A'])].groupby(['IATA_CODE', 'CANCELLATION_REASON']).sum().reset_index()

avoidable_cancellation_reasons = pd.merge(avoidable_cancellation_reasons, airlines, on='IATA_CODE')
print("A - Carrier; B - Weather; C - National Air System; D - Security")
pd.set_option('max_rows', 50)
avoidable_cancellation_reasons[["IATA_CODE", "AIRLINE", "CANCELLATION_REASON", "CANCELLED"]].sort_values(by=['CANCELLED'],ascending=[False])


# Lastly I wanted to look at what is the worst airline/month to fly and as expected it's the winter months, especially February which takes 6 of the top 10 spots.

# In[25]:


#Worst weather time to fly (2/3)
cancellation_reasons = flights.rename(index=str, columns={"AIRLINE": "IATA_CODE"})[["MONTH","CANCELLED","IATA_CODE","CANCELLATION_REASON"]]
unavoidable_cancellation_reasons = cancellation_reasons.loc[cancellation_reasons["CANCELLATION_REASON"].isin(['B'])].groupby(['IATA_CODE', 'MONTH']).sum().reset_index()

unavoidable_cancellation_reasons = pd.merge(unavoidable_cancellation_reasons, airlines, on='IATA_CODE')
pd.set_option('max_rows', 20)
unavoidable_cancellation_reasons[["IATA_CODE", "AIRLINE", 'MONTH', "CANCELLED"]].sort_values(by=['CANCELLED'],ascending=[False])

