#!/usr/bin/env python
# coding: utf-8

# ## Importing packages

# In[1]:


import sys
get_ipython().system('{sys.executable} -m pip install fpdf -q')
get_ipython().system('{sys.executable} -m pip install pandas -q')
get_ipython().system('{sys.executable} -m pip install plotly-express -q')
get_ipython().system('{sys.executable} -m pip install kaleido -q')


# In[2]:


from datetime import date
from pathlib import Path
import sqlite3
import pandas as pd
import pandas as pd
import plotly.express as px
#from fpdf import FDPF


# ## Define plotly template 

# In[3]:


plotly_template = 'presentation'


# In[4]:


current_dir = PATH(__file__).parent if "__file__" in locals() else Path.cwd()
database_path = r"C:\Users\Nicole\Desktop\stripe\stripe_proj.db"


# In[5]:


#step 3: Create/connect to a SQLite database
connection = sqlite3.connect('stripe_proj.db')


# In[6]:


#create connection to database 
conn = sqlite3.connect(database_path)


# ## Joining all three tables together

# In[7]:


query = """
SELECT date, platform_id, recipient_id, count, (count * amount) AS new_amount, country, industry FROM payouts
LEFT JOIN countries on payouts.recipient_id = countries.merchant_id 
LEFT JOIN industries on countries.merchant_id = industries.merchant_id

"""
data_df = pd.read_sql_query(query, conn)


# In[8]:


data_df.info()


# In[9]:


data_df['date'] = pd.to_datetime(data_df['date'])
data_df.head()


# In[10]:


data_df.set_index('date')
data_df.head()


# ## Amount of money to be paid to each country on Jan 1, 2019

# Assumtptions made: amount is equal to amount multiplied by count

# In[11]:


query = """
With ds AS (
SELECT date, platform_id, recipient_id, count, (count * amount) AS new_amount, country, industry FROM payouts
LEFT JOIN countries on payouts.recipient_id = countries.merchant_id
LEFT JOIN industries on countries.merchant_id = industries.merchant_id
)
SELECT country, SUM(ds.new_amount) AS total_amount_per_country
FROM ds
GROUP BY country  

"""
countries_df =  pd.read_sql_query(query, conn)
countries_df.set_index('country')


# In[13]:


#creating a visual
fig = px.bar(countries_df,
             x ='country',
             y ='total_amount_per_country',
             template = plotly_template,
             text = 'total_amount_per_country')

#update layout
fig.update_layout(
title = 'Total amount paid to each country EOY',
xaxis_title = 'Countries',
yaxis_title = 'Total amount paid',
    yaxis_tickprefix = '$s',)

fig.show()


# ## Checking to see number of industries currently for three mentioned industries
# 
# 

# Assumptions made: counting distinct platform id to see how many as there is a 1 to many relationship 
# Filter by industries

# In[14]:


query = """ With ds AS (
SELECT date, platform_id, recipient_id, count, (count * amount) AS new_amount, country, industry FROM payouts
LEFT JOIN countries on payouts.recipient_id = countries.merchant_id
LEFT JOIN industries on countries.merchant_id = industries.merchant_id
)
SELECT industry, COUNT(DISTINCT platform_id) AS platforms_per_industry
FROM ds
WHERE industry = 'Education'
OR industry = 'Travel & Hospitality'
OR industry = 'Food & Beverage'
OR industry = 'Tickets: concerts,sports,movies,conventions'
GROUP BY industry

"""
industries_df =  pd.read_sql_query(query, conn)
industries_df.head()


# In[15]:


#dropping Tickets:concerts, sports ... & Travel & Hospitality to create a new row 'Hotels, Restaurants & Leisure'
industries_df.drop([2, 3], axis =0, inplace = True) 
industries_df.head()


# In[16]:


industries_df.loc[2] = ['Hotels, Restaurants & Leisure', 15]
industries_df.set_index('industry', inplace = True)
industries_df.head()


# In[17]:


industries_df.insert(0,"platforms_per_industry_2019", [15, 40, 5], True)
industries_df.head()


# In[18]:


industries_df['platform_multiplier'] = industries_df['platforms_per_industry_2019']/ industries_df['platforms_per_industry']
industries_df


# In[ ]:


#in the above, we created a multiplier to see how much platforms industries are to grow in 2019. Based off this we can then multiply by projected growth.


# In[19]:


query = """With ds AS (
SELECT date, platform_id, recipient_id, count, (count * amount) AS new_amount, country, industry FROM payouts
LEFT JOIN countries on payouts.recipient_id = countries.merchant_id
LEFT JOIN industries on countries.merchant_id = industries.merchant_id
),
volumes AS(
SELECT date, industry, COUNT(recipient_id) AS daily_volume
FROM ds
WHERE industry = 'Education'
--OR industry = 'Travel & Hospitality'
--OR industry = 'Food & Beverage'
GROUP BY date
),
prev_volumes AS (
SELECT
*,
COALESCE (
LAG(daily_volume) OVER (ORDER BY date asc), 0) AS prev_daily_volume
FROM volumes
ORDER by date asc
),
growth AS(
SELECT *,
ROUND( 1 +
ROUND(daily_volume - prev_daily_volume) / prev_daily_volume *100, 2
)
AS daily_volume_growth_rate
FROM prev_volumes
ORDER BY date
)
SELECT industry, ROUND(AVG(daily_volume), 2) AS avg_daily_volume, ROUND(AVG(daily_volume_growth_rate),2) as avg_daily_growth_rate
FROM growth
"""

growth_df =  pd.read_sql_query(query, conn)


# In[20]:


#For education, random volume at a given future date = avg daily volume * avg daily growth * platform multiplier
future_daily_volume = growth_df['avg_daily_volume'] * growth_df['avg_daily_growth_rate']*industries_df['platform_multiplier'][0]
future_daily_volume


# In[21]:


#now we do the same for other industries
query = """With ds AS (
SELECT date, platform_id, recipient_id, count, (count * amount) AS new_amount, country, industry FROM payouts
LEFT JOIN countries on payouts.recipient_id = countries.merchant_id
LEFT JOIN industries on countries.merchant_id = industries.merchant_id
),
volumes AS(
SELECT date, industry, COUNT(recipient_id) AS daily_volume
FROM ds
WHERE 
--industry = 'Education'
--OR industry = 'Travel & Hospitality'
industry = 'Food & Beverage'
GROUP BY date
),
prev_volumes AS (
SELECT
*,
COALESCE (
LAG(daily_volume) OVER (ORDER BY date asc), 0) AS prev_daily_volume
FROM volumes
ORDER by date asc
),
growth AS(
SELECT *,
ROUND( 1 +
ROUND(daily_volume - prev_daily_volume) / prev_daily_volume, 2
)
AS daily_volume_growth_rate
FROM prev_volumes
ORDER BY date
)
SELECT industry, ROUND(AVG(daily_volume), 2) AS avg_daily_volume, ROUND(AVG(daily_volume_growth_rate),2) as avg_daily_growth_rate
FROM growth
"""

growth_df =  pd.read_sql_query(query, conn)
growth_df


# In[22]:


#For education, random volume at a given future date = avg daily volume * avg daily growth * platform multiplier
future_daily_volume = growth_df['avg_daily_volume'] * growth_df['avg_daily_growth_rate']*industries_df['platform_multiplier'][1]
future_daily_volume


# In[23]:


#now we do the same for other industries
query = """With ds AS (
SELECT date, platform_id, recipient_id, count, (count * amount) AS new_amount, country, industry FROM payouts
LEFT JOIN countries on payouts.recipient_id = countries.merchant_id
LEFT JOIN industries on countries.merchant_id = industries.merchant_id
),
volumes AS(
SELECT date, industry, COUNT(recipient_id) AS daily_volume
FROM ds
WHERE 
--industry = 'Education'
industry = 'Travel & Hospitality'
--industry = 'Food & Beverage'
GROUP BY date
),
prev_volumes AS (
SELECT
*,
COALESCE (
LAG(daily_volume) OVER (ORDER BY date asc), 0) AS prev_daily_volume
FROM volumes
ORDER by date asc
),
growth AS(
SELECT *,
ROUND( 1 +
ROUND(daily_volume - prev_daily_volume) / prev_daily_volume *100, 2
)
AS daily_volume_growth_rate
FROM prev_volumes
ORDER BY date
)
SELECT industry, ROUND(AVG(daily_volume), 2) AS avg_daily_volume, ROUND(AVG(daily_volume_growth_rate),2) as avg_daily_growth_rate
FROM growth
"""

growth_df =  pd.read_sql_query(query, conn)
growth_df


# In[24]:


#For education, random volume at a given future date = avg daily volume * avg daily growth * platform multiplier
future_daily_volume = growth_df['avg_daily_volume'] * growth_df['avg_daily_growth_rate']*industries_df['platform_multiplier'][2]
future_daily_volume


# In[25]:


#now we do the same for other industries
query = """With ds AS (
SELECT date, platform_id, recipient_id, count, (count * amount) AS new_amount, country, industry FROM payouts
LEFT JOIN countries on payouts.recipient_id = countries.merchant_id
LEFT JOIN industries on countries.merchant_id = industries.merchant_id
),
volumes AS(
SELECT date, industry, COUNT(recipient_id) AS daily_volume
FROM ds

WHERE industry = 'Tickets: concerts,sports,movies,conventions'
--industry = 'Education'
--industry = 'Travel & Hospitality'
--industry = 'Food & Beverage'
GROUP BY date
),
prev_volumes AS (
SELECT
*,
COALESCE (
LAG(daily_volume) OVER (ORDER BY date asc), 0) AS prev_daily_volume
FROM volumes
ORDER by date asc
),
growth AS(
SELECT *,
ROUND( 1 +
ROUND(daily_volume - prev_daily_volume) / prev_daily_volume *100, 2
)
AS daily_volume_growth_rate
FROM prev_volumes
ORDER BY date
)
SELECT industry, ROUND(AVG(daily_volume), 2) AS avg_daily_volume, ROUND(AVG(daily_volume_growth_rate),2) as avg_daily_growth_rate
FROM growth
"""

growth_df =  pd.read_sql_query(query, conn)
growth_df


# In[27]:


#For education, random volume at a given future date = avg daily volume * avg daily growth * platform multiplier
future_daily_volume = growth_df['avg_daily_volume'] * growth_df['avg_daily_growth_rate']*industries_df['platform_multiplier'][2]
future_daily_volume


# ## Things to consider: Takeaways
# 

# We should look at the growth rate per country to see any trends. In times when growth is low we can then investigate more granularly by industry. this will give stripe an indication to whether growth is related geographically and what potential economic events may traverse into industries.
