#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:14:41 2023

@author: ishratvasid
"""

import pandas as pd
import os
os.chdir("/Users/ishratvasid/Desktop/WQU/Capstone Project/Code/")

from tickers import tickers
from getFinancialData import getFinancialData
import company
from getFscore import getFscore

all_tickers = tickers()

year = 2010
sp500_tickers = all_tickers[(all_tickers['date'].dt.year < year) & (all_tickers['action'] == 'added')][['ticker','name']].reset_index(drop=True)

#a = getFinancialData(sp500_tickers, year)
companies = []
for m in  range(len(sp500_tickers)): 
    ticker = sp500_tickers.loc[m,'ticker']
    name = sp500_tickers.loc[m,'name']
    finData = getFinancialData(ticker, year)
    row = company.Company(name, ticker, finData[0], finData[1], finData[2])
    companies.append(row)
    
fscore = getFscore(companies)

