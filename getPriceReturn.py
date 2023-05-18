#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:13:51 2023

@author: ishratvasid
"""

import yfinance as yf
import numpy as np
import requests


def getYahooPriceReturn(tickers_list, startdate, enddate):
    
    # Get the data for this tickers from yahoo finance
    data = yf.download(tickers_list, startdate, enddate, auto_adjust=True)['Close']
    price_return = data.pct_change()
    return price_return

def getAPIPriceReturn(ticker, startdate, enddate, yourapikey):
    ret_dict = requests.get(
        f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={startdate}&to={enddate}&apikey={yourapikey}")
    ret_dict = ret_dict.json()
    if len(ret_dict) == 0:
        return np.nan
    else:
        start_price = ret_dict['historical'][-1]['adjClose']
        end_price = ret_dict['historical'][0]['adjClose']
        price_return = ((end_price-start_price)/start_price)*100
        return price_return