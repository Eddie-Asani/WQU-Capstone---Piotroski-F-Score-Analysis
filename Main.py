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

all_tickers = tickers()
date = '01-01-2010'        
sp500_tickersByDate = tickersByDate(all_tickers, date)

#a = getFinancialData(sp500_tickers, year)
companies = []
for m in  range(len(sp500_tickersByDate[0:5])): 
    ticker = sp500_tickersByDate.loc[m,'ticker']
    name = sp500_tickersByDate.loc[m,'name']
    finData = getFinancialData(ticker, int(date.split('-')[2]))
    row = company.Company(name, ticker, finData[0], finData[1], finData[2])
    companies.append(row)
    
fscore = getFscore(companies)
fscore['date'] = date
