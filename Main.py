#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:14:41 2023

@author: ishratvasid
"""

import pandas as pd
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
startdate = '2010-01-01'   
enddate = '2010-12-31'     

# Tickers as of start date
sp500_tickersByDate = tickersByDate(all_tickers, startdate)

# 9 Fundamental Indicator Values of Companies in S&P500
companies = []
for m in  range(len(sp500_tickersByDate[0:50])): 
    ticker = sp500_tickersByDate.loc[m,'ticker']
    name = sp500_tickersByDate.loc[m,'name']
    finData = getFinancialData(ticker, int(startdate.split('-')[0]), yourapikey)
    row = company.Company(name, ticker, finData[0], finData[1], finData[2] )
    companies.append(row)
   
# Get F-Score 
fscore = getFscore(companies)
fscore['date'] = startdate

# Get Stock Price Return data
for i in range(len(fscore)):
    ticker = fscore.loc[i,'Ticker']
    stock_ret = getAPIPriceReturn(ticker, startdate, enddate, yourapikey)
    fscore.loc[i,'Price_Ret'] = stock_ret


# import statsmodels.api as sm
# X = fscore[['ROA', 'CFO', 'dROA', 'Accrual', 'dLeverage','dLiquid', 'EQ_Offered', 'dMargin', 'dTurn']]
# y = fscore[['Price_Ret']]
# model = sm.OLS(y, X).fit()
# predictions = model.predict(X)
# model.summary()