#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:33:47 2023

@author: ishratvasid
"""

import requests
import numpy as np
import re


def getFinancialData(ticker, year, yourapikey):
    data = []
    i, j = 0, 0
    
    
    headers = requests.utils.default_headers() 
    headers.update(
        {
            'User-Agent': 'ishratvasid',
        }
    )
    # BalanceSheet
    BS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{ticker}?limit=400&apikey={yourapikey}",  headers=headers)
    BS = BS.json()

    # Income statement
    IS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}?limit=400&apikey={yourapikey}",  headers=headers)
    IS = IS.json()

    # Cashflow statement
    CF = requests.get(
        f'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{ticker}?limit=400&apikey={yourapikey}',  headers=headers)
    CF = CF.json()
    
    for a in range(len(BS['financials'])):
        if re.search(f'{year}-\d\d-\d\d', BS['financials'][a]['date']):
            i = a
            j = i + 1
#           k = i + 2
            break

    fin_cy = {'Date': IS["financials"][i]['date'],
              'Net Income': float(IS['financials'][i]['Net Income']),
              'Total Assets': float(BS["financials"][i]['Total assets']),
              'Operating Cash Flow': float(CF['financials'][i]["Operating Cash Flow"]) ,
              'Beginning Year Total Assets': float(BS['financials'][i]["Total assets"]),
              'Long Term Debt': float(BS["financials"][i]['Long-term debt']),
              'Current Assets': float(BS["financials"][i]['Total current assets']),
              'Current Liabilities': float(BS["financials"][i]['Total current liabilities']),
              'Weighted Average Shares Out': float(IS['financials'][i]['Weighted Average Shs Out']),
              'Gross Margin': float(IS['financials'][i]['Gross Margin']),
              'Revenue': float(IS['financials'][i]['Revenue'])
              }

    fin_py = {'Date': IS["financials"][j]['date'],
              'Net Income': float(IS['financials'][j]['Net Income']) ,
              'Total Assets': float(BS["financials"][j]['Total assets']),
              'Operating Cash Flow': float(CF['financials'][j]["Operating Cash Flow"]) ,
              'Beginning Year Total Assets': float(BS['financials'][j]["Total assets"]),
              'Long Term Debt': float(BS["financials"][j]['Long-term debt']),
              'Current Assets': float(BS["financials"][j]['Total current assets']),
              'Current Liabilities': float(BS["financials"][j]['Total current liabilities']),
              'Weighted Average Shares Out': float(IS['financials'][j]['Weighted Average Shs Out']),
              'Gross Margin': float(IS['financials'][j]['Gross Margin']),
              'Revenue': float(IS['financials'][j]['Revenue']) 
              }

    # fin_py2 = {'Date': IS["financials"][k]['date'],
    #            'Net Income': float(IS['financials'][k]['Net Income']),
    #            'Total Assets': float(BS["financials"][k]['Total assets']),
    #            'Operating Cash Flow': float(CF['financials'][k]["Operating Cash Flow"]) ,
    #            'Beginning Year Total Assets': float(BS['financials'][k]["Total assets"]),
    #            'Long Term Debt': float(BS["financials"][k]['Long-term debt']),
    #            'Current Assets': float(BS["financials"][k]['Total current assets']),
    #            'Current Liabilities': float(BS["financials"][k]['Total current liabilities']),
    #            'Weighted Average Shares Out': float(IS['financials'][k]['Weighted Average Shs Out']),
    #            'Gross Margin': float(IS['financials'][k]['Gross Margin']),
    #            'Revenue': float(IS['financials'][k]['Revenue']) 
    #            }
    data.append(fin_cy)
    data.append(fin_py)
#   data.append(fin_py2)

    return data