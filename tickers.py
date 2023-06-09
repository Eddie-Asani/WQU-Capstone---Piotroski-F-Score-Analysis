#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:41:08 2023

@author: ishratvasid
'/Users/ishratvasid/Desktop/WQU/Capstone Project'
"""

from datetime import datetime
import pandas as pd

def tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    data = pd.read_html(url)

    # Get current S&P table and set header column
    sp500 = data[0].iloc[:, [0,1,5,6]]
    sp500.columns = ['ticker', 'name', 'date' , 'cik']

    # Get rows where date is missing or not formatted correctly.
    mask = sp500['date'].str.strip().str.fullmatch('\d{4}-\d{2}-\d{2}')
    mask.loc[mask.isnull()] = False
    mask = mask[mask == False].index

    #Fill the missing data
    current = sp500.copy()
    current.loc[mask, 'date'] = '1990-01-01'
    current.loc[:, 'date'] = pd.to_datetime(current['date'])
    current.loc[:, 'cik'] = current['cik'].apply(str).str.zfill(10)

    # Get the adjustments dataframe and rename columns
    adjustments = data[1]
    columns = ['date', 'ticker_added','name_added', 'ticker_removed', 'name_removed', 'reason']
    adjustments.columns = columns

    # Create additions dataframe.
    additions = adjustments[~adjustments['ticker_added'].isnull()][['date','ticker_added', 'name_added']]
    additions.columns = ['date','ticker','name']
    additions['action'] = 'added'

    # Create removals dataframe.
    removals = adjustments[~adjustments['ticker_removed'].isnull()][['date','ticker_removed','name_removed']]
    removals.columns = ['date','ticker','name']
    removals['action'] = 'removed'

    # Merge the additions and removals into one dataframe.
    historical = pd.concat([additions, removals])
    historical.loc[:, 'date'] = pd.to_datetime(current['date'])
    
    #let’s add any tickers in the S&P 500 index but not in Wikipedia history.
    missing = current[~current['ticker'].isin(historical['ticker'])].copy()
    missing['action'] = 'added'
    missing = missing[['date','ticker','name','action', 'cik']]
    missing.loc[:, 'cik'] = current['cik'].apply(str).str.zfill(10)

    #Merge and Dedup the Data
    sp500_history = pd.concat([historical, missing])
    sp500_history = sp500_history.sort_values(by=['date','ticker'], ascending=[False, True])
    sp500_history = sp500_history.drop_duplicates(subset=['date','ticker']).reset_index(drop=True)

    return sp500_history

def tickersByDate(ticker_df, date):
    day = date.split('-')
    date = f"{day[1]}-{day[2]}-{day[0]}"
    #dt = datetime.strptime(date,'%d-%m-%Y').strftime('%d-%m-%Y')
    all_tickers_tilldate = ticker_df[ticker_df['date']< date] 
    all_tickers_tilldate = all_tickers_tilldate.reindex(index=all_tickers_tilldate.index[::-1])

    index_ticker = pd.DataFrame()
    for i in all_tickers_tilldate['date'].unique():
        date_df = all_tickers_tilldate[all_tickers_tilldate['date'] == i]
        if i == '1957-03-04':
            date_df = date_df[date_df['action'] != 'removed']
            index_ticker = date_df
        else:
            added_df = date_df[date_df['action'] == 'added']
            index_ticker = index_ticker.append(added_df)
            removed_df = date_df[date_df['action'] == 'removed']
            index_ticker = index_ticker[~index_ticker['ticker'].isin(removed_df['ticker'])]

    return index_ticker.reset_index(drop=True) 

