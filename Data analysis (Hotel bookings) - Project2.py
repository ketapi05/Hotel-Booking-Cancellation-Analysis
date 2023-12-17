#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries
#         

# In[114]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading the data set

# In[115]:


df = pd.read_csv(r'C:\Users\Sisodiya\Downloads\hotel_booking.csv\hotel_booking.csv')


# In[117]:


df.shape


# # Exploratory data analysis and data cleaning
#     

# In[118]:


df.head()


# In[119]:


df.shape


# In[120]:


df.columns


# In[121]:


df.info()


# In[122]:


#reservation_status_date "object" ke form me hai, usko "datetime" me convert krna pdega
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[123]:


df.info()


# In[124]:


df.describe(include = 'object')
#uppr wali line sirf 'object' column ke data ko return kr rhi hai


# In[125]:


for col in df.describe(include = 'object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[126]:


#check for missing values
df.isnull().sum()


# In[127]:


#'agent', 'company' drop kr do
df.drop(['agent', 'company'], axis = 1, inplace = True)
df.dropna(inplace = True)


# In[128]:


df.isnull().sum()


# In[129]:


df.describe()


# In[130]:


df = df[df['adr']<5000]   #we remove outliers by doing this


# # Data analysis and visulaliszations

# In[131]:


canc_percen = df['is_canceled'].value_counts(normalize = True)
canc_percen


# In[132]:


#ab hum canc_percen ko print krke, visualize krenege
print(canc_percen)
plt.figure(figsize = (5,4))
plt.title('reservation_status')
plt.bar(['not canceled', 'cancelled'], df['is_canceled'].value_counts(), edgecolor = 'k', width = 0.7)
plt.show()


# In[133]:


plt.figure(figsize = (8, 4))
axl = sns.countplot(x = 'hotel', hue = 'is_canceled', data = df, palette = 'Blues')
plt.title('Reservation status in different hotels', size = 20)
plt.xlabel('Hotel')
plt.ylabel('No. of reservations')


# In[134]:


#now we need to know- how many percentage of booking in resort hotel are cancelled
resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)


# In[135]:


#from upper result it can be said that approx 28% of booking in resort hotel are getting cancelled


# In[136]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[137]:


#from uppper result it can be said that approx 41% of booking are getting cancelled


# In[138]:


#Now we will see, does price has effect on city/resort hotel cancellation
resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[139]:


plt.figure(figsize = (20, 8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label = 'city Hotel')
plt.legend(fontsize = 20)
plt.show()


# In[140]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize = (16, 8))
axl = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette = 'bright')
legend_labels,_ = axl. get_legend_handles_labels()
axl.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status per month', size = 20)
plt.xlabel('Month')
plt.ylabel('Number of Reservations')
plt.legend('not cancelled', 'cancelled')
plt.show()


# In[141]:


#now let's plot average daily rate for each month....we need to check price has effect on cancellation rate or not
plt.figure(figsize = (15, 8))
plt.title('ADR per month', fontsize = 30)
sns.barplot(x='month', y= 'adr', data = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.legend(fontsize = 20)
plt.show()


# In[142]:


#the above two graphs prove the things that if adr is high then cancellation rates are also high for that month.


# In[143]:


#now we will analyse for the top 10 countries...which has highest cancellation
cancelled_data = df[df['is_canceled'] == 1]
top_10_country = cancelled_data['country'].value_counts()[:10]
plt.figure(figsize = (8, 8))
plt.title('Top 10 countries with reservation cancelled')
plt.pie(top_10_country, autopct = '%.2f', labels = top_10_country.index)
plt.show()


# In[144]:


#we observed that: Portugal countries has highest cancellation rate
#suggestion - hotels should increase facilities, promotional disc should be given
#do more advertising and give more facilities in low prices


# In[145]:


#now we will check where does this booking is coming from
df['market_segment'].value_counts()


# In[146]:


#To see above data in terms of percentage
df['market_segment'].value_counts(normalize = True)


# In[147]:


#now let's see cancellation numbers
cancelled_data['market_segment'].value_counts(normalize = True)


# In[148]:


#possible reasons for max cancellation of 'online TA' booking
#maybe the hotel we saw in online booking differ fromo actual


# In[151]:


#let check if adr{cancelled reserv} is higher than adr{non cancelled reserv}
cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace = True)
cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

not_cancelled_data = df[df['is_canceled'] == 0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace = True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure(figsize = (20, 6))
plt.title('Average Daily Rate', fontsize = 30)
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label = 'not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend()
plt.show()
    


# In[152]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date'] > '2016') & (cancelled_df_adr['reservation_status_date'] < '2017-09') ]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date'] > '2016') & (not_cancelled_df_adr['reservation_status_date'] < '2017-09')]


# In[153]:


plt.figure(figsize = (20, 6))
plt.title('Average daily rate', fontsize = 30)
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label = 'not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend(fontsize = 20)


# In[ ]:


#Here our data analysis project is complete!!!!!!!!!!!!!

