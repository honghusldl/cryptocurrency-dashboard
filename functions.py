import os
import numpy as np 
import pandas as pd 
from datetime import datetime

def load_data():
    # import data
    dateparse = lambda dates: [datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
    with open('currency_edited.csv','r') as f:
        data = pd.read_csv(f,index_col=None,parse_dates=['Date'],date_parser=dateparse)

    return data

  # data imported
def get_df(df):
    names = list(df['Name'].unique())
    names.sort()
    columns = list(df.columns)[2:6]
    # return names

    df_group = df.groupby('Name')
    min_date = df_group['Date'].min()
    max_date = df_group['Date'].max()
    min_max_date = pd.merge(min_date,max_date, on='Name')
    min_max_date.columns = ['First Day','Last Day']
    min_max_date['First Day'] = min_max_date['First Day'].dt.date
    min_max_date['Last Day'] = min_max_date['Last Day'].dt.date
    min_max_date['Duration'] = min_max_date['Last Day'] - min_max_date['First Day']
    min_max_date['Duration'] = min_max_date['Duration'].astype('timedelta64[D]')
    min_max_date['Duration'] = min_max_date['Duration'].astype(int)
    # return min_max_date

    return names, min_max_date,columns

def get_month(year):
    if year ==2021:
        month = list(range(1,8))
    else:
      month = list(range(1,13))

    return month

def get_day(year,month):
    if (month == 2 & year == 2020):
        day = list(range(1,30))
    elif (year == 2021 & month == 7):
        day = list(range(1,7))
    elif month in [1,3,5,7,8,10,12]:
        day = list(range(1,32))
    elif month in [4,6,9,11]:
        day = list(range(1,31))
    else:    
        day = list(range(1,29))

    return day
def get_percentage(df):
    df = df[['Name','Market_Capitalization']]
    total = df['Market_Capitalization'].sum()
    df['Percentage'] = df['Market_Capitalization'].apply(lambda x: x/total)
    df['Percentage'] = (df['Percentage']*100).apply(lambda x: f'{x:.3f}') + '%'
    df.set_index('Name',drop = True,inplace=True)
    df.drop(columns = 'Market_Capitalization',inplace=True)
    df.sort_values(by = ['Percentage'],ascending = False,inplace =True)
    return df

def get_df_pv(df):
    df_pv = df[df['Date']>'2016-12-31']
    return df_pv
