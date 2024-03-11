#!/usr/bin/env python
# coding: utf-8

# In[75]:


import pandas as pd


# In[7]:


import warnings
warnings.filterwarnings('ignore')


# In[74]:


# data analysis libraries and for visualisation
import numpy as np, pandas as pd
from matplotlib import pyplot as plt


# In[72]:


import seaborn as sns


# In[14]:


#Importing the data

appl_data = pd.read_csv("Downloads\\application_data.csv")
previous_appl = pd.read_csv("Downloads\\previous_application.csv")
col_description = pd.read_csv("Downloads\\columns_description.csv", encoding='latin1',skiprows=1)


# In[287]:


#First five rows of the data
appl_data.head()
previous_appl.head()
col_description.head()


# In[20]:


#Dimensions of the data
appl_data.shape
previous_appl.shape
col_description.shape


# In[25]:


# Dropping the first column as it does not help with any data
col_description.drop(['1'],axis=1,inplace=True)
co1_description.head()
display(col_description)


# In[26]:


#################Application data###################
# Cleaning the missing data

# listing the null values columns having more than 30% 

empty_col=appl_data.isnull().sum()
empty_col=empty_col[empty_col.values>(0.3*len(empty_col))]
len(empty_col)


# In[27]:


# Removing 64 columns of null data
empty_col = list(empty_col[empty_col.values>=0.3].index)
appl_data.drop(labels=empty_col,axis=1,inplace=True)
print(len(empty_col))


# In[28]:


# Checking the columns having less null percentage

appl_data.isnull().sum()/len(appl_data)*100


# In[29]:


# Filling missing values with median as it cannot be empty

missing_values=appl_data['AMT_ANNUITY'].median()

appl_data.loc[appl_data['AMT_ANNUITY'].isnull(),'AMT_ANNUITY']=missing_values


# In[30]:


# checking the column for null values

appl_data.isnull().sum()


# In[31]:


# Removing rows having null values which have more or equal to 30% in the data

row=appl_data.isnull().sum(axis=1)
row=list(row[row.values>=0.3*len(appl_data)].index)
appl_data.drop(labels=row,axis=0,inplace=True)
print(len(row))


# In[33]:


#  Removing the columns which are not useful from dataset

rem_col=['FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE',
       'FLAG_PHONE', 'FLAG_EMAIL','REGION_RATING_CLIENT','REGION_RATING_CLIENT_W_CITY','FLAG_EMAIL','CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT',
       'REGION_RATING_CLIENT_W_CITY','DAYS_LAST_PHONE_CHANGE', 'FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3','FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6',
       'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9','FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12',
       'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15','FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18',
       'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21']

appl_data.drop(labels=rem_col,axis=1,inplace=True)


# In[35]:


# checking if columns having any 'XNA' values
    
# For Gender column

appl_data[appl_data['CODE_GENDER']=='XNA'].shape


# In[37]:


# For Organization column

appl_data[appl_data['ORGANIZATION_TYPE']=='XNA'].shape


# In[39]:


# Checking Gender column for the number of females and males data

appl_data['CODE_GENDER'].value_counts()


# In[41]:


# Updating the null column 'CODE_GENDER' with "F" 

appl_data.loc[appl_data['CODE_GENDER']=='XNA','CODE_GENDER']='F'
appl_data['CODE_GENDER'].value_counts()


# In[43]:


# Describing the organization type column

appl_data['ORGANIZATION_TYPE'].describe()


# In[46]:


# Dropping the rows which have 'XNA' values in the organization type column

appl_data=appl_data.drop(appl_data.loc[appl_data['ORGANIZATION_TYPE']=='XNA'].index)
appl_data[appl_data['ORGANIZATION_TYPE']=='XNA'].shape


# In[47]:


# Converting all variable into numeric in the dataset

ncols=['TARGET','CNT_CHILDREN','AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY','REGION_POPULATION_RELATIVE','DAYS_BIRTH',
                'DAYS_EMPLOYED','DAYS_REGISTRATION','DAYS_ID_PUBLISH','HOUR_APPR_PROCESS_START','LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY',
       'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY']

appl_data[ncols]=appl_data[ncols].apply(pd.to_numeric)
appl_data.head(3)


# In[48]:


# Creating different category for Credit amount

cred_amt = [0,150000,200000,250000,300000,350000,400000,450000,500000,550000,600000,650000,700000,750000,800000,850000,900000,1000000000]
amt = ['0-150000', '150000-200000','200000-250000', '250000-300000', '300000-350000', '350000-400000','400000-450000',
        '450000-500000','500000-550000','550000-600000','600000-650000','650000-700000','700000-750000','750000-800000',
        '800000-850000','850000-900000','900000 and above']

appl_data['AMT_CREDIT_RANGE']=pd.cut(appl_data['AMT_CREDIT'],bins=cred_amt,labels=amt)


# In[49]:


# Diffrentiating and dividing the dataset into two datasets of client with payment difficulties as candidate1 and others as candidate0

candidate0_appl_data=appl_data.loc[appl_data["TARGET"]==0]
candidate1_appl_data=appl_data.loc[appl_data["TARGET"]==1]


# In[51]:


# Calculating error percentage
    
# Since the majority is candidate0 rather than candidate1

round(len(candidate0_appl_data)/len(candidate1_appl_data),2)


# In[141]:


#Univariate Analysis  for candidate0(candidates with no payment difficulties)

def uniplot(appl_data,col,title,hue =None):
   
    
    temp = pd.Series(data = hue)
    fig, x = plt.subplots()
    plt.xticks(rotation=90)
    plt.yscale('log')
    plt.title(title)
    x = sns.countplot(data = appl_data, x= col, order=appl_data[col].value_counts().index,hue = hue,palette='Accent') 
        
    plt.show()


# In[142]:


# PLotting for Gender

plt.figure(figsize=(6,4)) 
sns.countplot('CODE_GENDER',data=appl_data) 
plt.show()


# In[190]:


# Plotting for Income type


uniplot(candidate0_appl_data,col='NAME_INCOME_TYPE',title='Distribution of Income type',hue='CODE_GENDER')


# In[191]:


# Plotting for Contract type

uniplot(candidate0_appl_data,col='NAME_CONTRACT_TYPE',title='Distribution of contract type',hue='CODE_GENDER')


# In[194]:


# Plotting for Organization type 

plt.figure(figsize=(18,18))
plt.xscale('log')
plt.rcParams["axes.titlesize"] = 20
plt.title("Distribution of Organization(candidate0)")
sns.countplot(data=candidate0_appl_data,y='ORGANIZATION_TYPE',order=candidate0_appl_data['ORGANIZATION_TYPE'].value_counts().index,palette='YlOrRd')

plt.show()


# In[189]:


# Univariate Analysis for Candidate 1(client with payment difficulties)

# PLotting for income range

uniplot(candidate1_appl_data,col='NAME_INCOME_TYPE',title='Distribution of income',hue='CODE_GENDER')
candidate1_appl_data.NAME_CONTRACT_TYPE.value_counts(normalize = True).plot.bar()


# In[193]:


# Plotting for Organization type

plt.figure(figsize=(18,18))
plt.xscale('log')
plt.rcParams["axes.titlesize"] = 20

plt.title("Distribution of Organization(candidate 1)")

sns.countplot(data=candidate1_appl_data,y='ORGANIZATION_TYPE',order=candidate1_appl_data['ORGANIZATION_TYPE'].value_counts().index,palette='Spectral')

plt.show()


# In[195]:


# correlation for numerical columns for both candidate 0 and 1 

candidate0_corr=candidate0_appl_data.iloc[0:,2:]
candidate1_corr=candidate1_appl_data.iloc[0:,2:]

candidate0=candidate0_corr.corr(method='spearman')
candidate1=candidate1_corr.corr(method='spearman')


# In[199]:


#correlation for candidates 0
candidate0
#correlation for candidates 1
candidate1


# In[207]:


# Plotting correlation with heat map as it is the best choice to visulaize

def candidates_corr(data,title):
    plt.figure(figsize=(15, 10))

# heatmap with a color map of choice

    sns.heatmap(data, cmap="Blues_r",annot=False)

    plt.title(title)
    plt.show()


# In[209]:


# For Candidate 0

candidates_corr(data=candidate0,title='Correlation for candidate 0')


# In[211]:


#for candidate 1
candidates_corr(data=candidate1,title='Correlation for candidate 1')


# In[217]:


######Univariate analysis for variables

# Box plotting for univariate variables analysis


# In[215]:


# Distribution of income amount
sns.boxplot(candidate0_appl_data.AMT_INCOME_TOTAL)
title='Distribution of income amount'
plt.show()


# In[220]:


# Disrtibution of credit amount
def univariate_numerical(data,col,title):
    plt.title(title)
    sns.boxplot(data =candidate0_appl_data, x=col)
    plt.show()

univariate_numerical(data=candidate0_appl_data,col='AMT_CREDIT',title='Distribution of credit amount')


# In[222]:


# Distribution of anuuity amount
sns.boxplot(candidate0_appl_data.AMT_ANNUITY)
title='Distribution of amount annuity'
plt.show()


# In[224]:


#For candidate 1 - Finding any outliers

# Distribution of income amount

univariate_numerical(data=candidate1_appl_data,col='AMT_INCOME_TOTAL',title='Distribution of income amount')


# In[226]:


# Distribution of credit amount
sns.boxplot(candidate1_appl_data.AMT_CREDIT)
title='Distribution of amount credit'
plt.show()


# In[228]:


# Distribution of Annuity amount
sns.boxplot(candidate1_appl_data.AMT_ANNUITY)
title='Distribution of amount Annuity'
plt.show()


# In[272]:


#Bivariate analysis

#For candidate 0

# Bar plotting for Credit amount

plt.figure(figsize=(8,8))
plt.xticks(rotation=45)
sns.barplot(data =candidate0_appl_data, x='NAME_EDUCATION_TYPE',y='AMT_CREDIT', hue ='NAME_FAMILY_STATUS')
plt.title('Credit amount vs Education Status')
plt.show()


# In[275]:


# Bar plotting for Income amount 

plt.figure(figsize=(8,8))
plt.xticks(rotation=45)
sns.barplot(data =candidate0_appl_data, x='NAME_EDUCATION_TYPE',y='AMT_INCOME_TOTAL', hue ='NAME_FAMILY_STATUS')
plt.title('Income amount vs Education Status')
plt.show()


# In[269]:


#For candidate 1

# Bar plotting for Credit amount

plt.figure(figsize=(8,8))
plt.xticks(rotation=45)
sns.barplot(data =candidate1_appl_data, x='NAME_EDUCATION_TYPE',y='AMT_CREDIT', hue ='NAME_FAMILY_STATUS')
plt.title('Credit amount vs Education Status')
plt.show()


# In[276]:


# Bar plotting for Income amount in logarithmic scale

plt.figure(figsize=(8,4))
plt.xticks(rotation=45)
sns.barplot(data =candidate1_appl_data, x='NAME_EDUCATION_TYPE',y='AMT_INCOME_TOTAL', hue ='NAME_FAMILY_STATUS')
plt.title('Income amount vs Education Status')
plt.show()


# In[ ]:


################previous  application######################


# In[243]:


# Cleaning the missing data

# listing the null values columns having more than 30%

emp_prev=previous_appl.isnull().sum()
emp_prev=emp_prev[emp_prev.values>(0.3*len(emp_prev))]
len(emp_prev)


# In[249]:


# Removing those 15 columns

emp_prev = list(emp_prev[emp_prev.values>=0.3].index)
previous_appl.drop(labels=emp_prev,axis=1,inplace=True)
previous_appl.shape


# In[248]:


# Removing the column values of 'XNA' and 'XAP'

previous_appl=previous_appl.drop(previous_appl[previous_appl['NAME_CASH_LOAN_PURPOSE']=='XNA'].index)
previous_appl=previous_appl.drop(previous_appl[previous_appl['NAME_CASH_LOAN_PURPOSE']=='XNA'].index)
previous_appl=previous_appl.drop(previous_appl[previous_appl['NAME_CASH_LOAN_PURPOSE']=='XAP'].index)

previous_appl.shape


# In[251]:


# Joining the Application dataset with previous application dataset

new_set=pd.merge(left=appl_data,right=previous_appl,how='inner',on='SK_ID_CURR',suffixes='_x')


# In[253]:


# Renaming the column names after merging

Bank = new_set.rename({'NAME_CONTRACT_TYPE_' : 'NAME_CONTRACT_TYPE','AMT_CREDIT_':'AMT_CREDIT','AMT_ANNUITY_':'AMT_ANNUITY',
                         'WEEKDAY_APPR_PROCESS_START_' : 'WEEKDAY_APPR_PROCESS_START',
                         'HOUR_APPR_PROCESS_START_':'HOUR_APPR_PROCESS_START','NAME_CONTRACT_TYPEx':'NAME_CONTRACT_TYPE_PREV',
                         'AMT_CREDITx':'AMT_CREDIT_PREV','AMT_ANNUITYx':'AMT_ANNUITY_PREV',
                         'WEEKDAY_APPR_PROCESS_STARTx':'WEEKDAY_APPR_PROCESS_START_PREV',
                         'HOUR_APPR_PROCESS_STARTx':'HOUR_APPR_PROCESS_START_PREV'}, axis=1)


# In[255]:


# Removing unwanted columns 

Bank.drop(['SK_ID_CURR','WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START','REG_REGION_NOT_LIVE_REGION', 
              'REG_REGION_NOT_WORK_REGION','LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY',
              'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY','WEEKDAY_APPR_PROCESS_START_PREV',
              'HOUR_APPR_PROCESS_START_PREV', 'FLAG_LAST_APPL_PER_CONTRACT','NFLAG_LAST_APPL_IN_DAY'],axis=1,inplace=True)


# In[259]:


#Performing univariate analysis

# Distribution of contract status
plt.figure(figsize=(10,10))
plt.xticks(rotation=90)
plt.xscale('log')
plt.title('Distribution of contract status with purposes')
x = sns.countplot(data = Bank, y= 'NAME_CASH_LOAN_PURPOSE', 
                   order=Bank['NAME_CASH_LOAN_PURPOSE'].value_counts().index,hue = 'NAME_CONTRACT_STATUS',palette='Reds') 


# In[262]:


# Distribution of purposes

plt.figure(figsize=(10,10))
plt.xscale('log')
plt.title('Distribution of purposes with target ')
x = sns.countplot(data = Bank, y= 'NAME_CASH_LOAN_PURPOSE', 
                   order=Bank['NAME_CASH_LOAN_PURPOSE'].value_counts().index,hue = 'TARGET',palette='Greens') 


# In[284]:


#Performing bivariate analysis

# bar plotting for Credit amount 

plt.figure(figsize=(15,10))
plt.xticks(rotation=90)
plt.yscale('log')
sns.barplot(data =Bank, x='NAME_CASH_LOAN_PURPOSE',hue='NAME_INCOME_TYPE',y='AMT_CREDIT_PREV')
plt.title('Prev Credit amount vs Loan Purpose')
plt.show()


# In[267]:


# Bar plotting for Credit amount prev vs Housing type in logarithmic scale

plt.figure(figsize=(5,5))
plt.xticks(rotation=90)
sns.barplot(data =Bank, y='AMT_CREDIT_PREV',hue='TARGET',x='NAME_HOUSING_TYPE')
plt.title('Prev Credit amount vs Housing type')
plt.show()

