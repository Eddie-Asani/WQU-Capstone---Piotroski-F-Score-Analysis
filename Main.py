#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:14:41 2023

@author: ishratvasid
"""

#import pandas as pd
from tqdm import tqdm
import os
os.chdir("/Users/ishratvasid/Desktop/GitHub/WQU-Capstone---Piotroski-F-Score-Analysis/")

from tickers import tickers
from tickers import tickersByDate
from getFinancialData import getFinancialData
import company
from getFscore import getFscore
from getPriceReturn import getAPIPriceReturn

yourapikey = 'a9825b793634b1fd7b14ed94547c0849'

# Get all tickers from Wikipedia
all_tickers = tickers()

# Time Period
tdate = '2022-01-01'   
pydate = '2021-01-01' #Previous Year Date    

# Tickers as of start date
sp500_tickersByDate = tickersByDate(all_tickers, tdate)

# 9 Fundamental Indicator Values of Companies in S&P500
companies = []
for m in  tqdm(range(len(sp500_tickersByDate))):     
    ticker = sp500_tickersByDate.loc[m,'ticker']
    # if ticker in ['PCLN','FOX','ESV','CEG','IR']:
    #     continue
   
    name = sp500_tickersByDate.loc[m,'name']
    try:
        finData = getFinancialData(ticker, int(tdate.split('-')[0]), yourapikey)
        row = company.Company(name, ticker, finData[0], finData[1] ) 
    except IndexError:
        print(m,' -- ', ticker, ' -- IndexError')
        continue
    except KeyError:
        print(m,' -- ', ticker, ' -- KeyError')
        continue
    except ValueError:
        print(m,' -- ', ticker, ' -- ValueError')
        continue
    except ZeroDivisionError:
        print(m,' -- ', ticker, ' -- ZeroDivisionError')
        continue
    except TypeError:
        print(m,' -- ', ticker, ' -- TypeError')
        continue
    else: 
        print(m,' --- ', ticker)
        companies.append(row)
   
# Get F-Score 
fscore = getFscore(companies)
fscore['date'] = tdate

# Get Stock Price Return data
for i in tqdm(range(len(fscore))):
    print(i,' --- ', ticker)
    ticker = fscore.loc[i,'Ticker']
    stock_ret = getAPIPriceReturn(ticker, pydate, tdate, yourapikey)
    fscore.loc[i,'Price_Ret'] = stock_ret

fscore = fscore[~fscore['Price_Ret'].isna()]
