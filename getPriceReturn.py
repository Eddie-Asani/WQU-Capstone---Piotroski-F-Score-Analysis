#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:13:51 2023

@author: ishratvasid
"""

import yfinance as yf


def getPriceReturn(tickers_list, startdate, enddate):
    
    # Get the data for this tickers from yahoo finance
    data = yf.download(tickers_list, startdate, enddate, auto_adjust=True)['Close']
    price_return = data.pct_change()
    return price_return