#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:33:47 2023

@author: ishratvasid
"""

import requests
#import json
import re


def getFinancialData(ticker, year):
    yourapikey = 'a9825b793634b1fd7b14ed94547c0849'
    data = []
    i, j, k = 0, 0, 0
    # BalanceSheet
    BS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{ticker}?limit=400&apikey={yourapikey}")
    BS = BS.json()

    # Income statement
    IS = requests.get(
        f"https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}?limit=400&apikey={yourapikey}")
    IS = IS.json()

    # Cashflow statement
    CF = requests.get(
        f'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{ticker}?limit=400&apikey={yourapikey}')
    CF = CF.json()
    
    
    for a in range(len(BS['financials'])):
        if re.search(f'{year}-\d\d-\d\d', BS['financials'][a]['date']):
            i = a
            j = i + 1
            k = i + 2
            break

    # Calculated Income Items
    # Current Year
    revenue = float(IS['financials'][i]['Revenue'])
    gross_margin = float(IS['financials'][i]['Gross Margin']) 
    net_income = float(IS['financials'][i]['Net Income']) 
    
    # Past Year
    revenue_py = float(IS['financials'][j]['Revenue']) 
    gross_margin_py = float(IS['financials'][j]['Gross Margin'])
    net_income_py = float(IS['financials'][j]['Net Income']) 
    
    # Past Year 2
    revenue_py2 = float(IS['financials'][k]['Revenue']) 
    gross_margin_py2 = float(IS['financials'][k]['Gross Margin'])
    net_income_py2 = float(IS['financials'][k]['Net Income'])
    
    # Calculated Cashflow Items
    # Current Year
    cashflow_op = float(CF['financials'][i]["Operating Cash Flow"]) 

    # Past Year
    cashflow_op_py = float(CF['financials'][j]["Operating Cash Flow"]) 

    # Past Year2
    cashflow_op_py2 = float(CF['financials'][k]["Operating Cash Flow"]) 

    # Calculated Balance Items
    # Current Year
    begYearTotalAssets = float(BS['financials'][i]["Total assets"])

    # Past Year
    begYearTotalAssets_py = float(BS['financials'][j]["Total assets"])

    # Past Year2
    begYearTotalAssets_py2 = float(BS['financials'][k]["Total assets"])

    fin_cy = {'Date': IS["financials"][i]['date'],
              'Net Income': net_income,
              'Total Assets': float(BS["financials"][i]['Total assets']),
              'Operating Cash Flow': cashflow_op,
              'Beginning Year Total Assets': begYearTotalAssets,
              'Long Term Debt': float(BS["financials"][i]['Long-term debt']),
              'Current Assets': float(BS["financials"][i]['Total current assets']),
              'Current Liabilities': float(BS["financials"][i]['Total current liabilities']),
              'Weighted Average Shares Out': float(IS['financials'][i]['Weighted Average Shs Out']),
              'Gross Margin': gross_margin,
              'Revenue': revenue
              }

    fin_py = {'Date': IS["financials"][j]['date'],
              'Net Income': net_income_py,
              'Total Assets': float(BS["financials"][j]['Total assets']),
              'Operating Cash Flow': cashflow_op_py,
              'Beginning Year Total Assets': begYearTotalAssets_py,
              'Long Term Debt': float(BS["financials"][j]['Long-term debt']),
              'Current Assets': float(BS["financials"][j]['Total current assets']),
              'Current Liabilities': float(BS["financials"][j]['Total current liabilities']),
              'Weighted Average Shares Out': float(IS['financials'][j]['Weighted Average Shs Out']),
              'Gross Margin': gross_margin_py,
              'Revenue': revenue_py
              }

    fin_py2 = {'Date': IS["financials"][k]['date'],
               'Net Income': net_income_py2,
               'Total Assets': float(BS["financials"][k]['Total assets']),
               'Operating Cash Flow': cashflow_op_py2,
               'Beginning Year Total Assets': begYearTotalAssets_py2,
               'Long Term Debt': float(BS["financials"][k]['Long-term debt']),
               'Current Assets': float(BS["financials"][k]['Total current assets']),
               'Current Liabilities': float(BS["financials"][k]['Total current liabilities']),
               'Weighted Average Shares Out': float(IS['financials'][k]['Weighted Average Shs Out']),
               'Gross Margin': gross_margin_py2,
               'Revenue': revenue_py2
               }
    data.append(fin_cy)
    data.append(fin_py)
    data.append(fin_py2)

    return data