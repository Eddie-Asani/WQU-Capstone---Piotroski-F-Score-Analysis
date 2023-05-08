#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:10:10 2023

@author: ishratvasid
"""

import pandas as pd
from fscore import calcF_score

def getFscore(companies):
    formateData = []
    for company in companies:
        info = {
            'Ticker': company.ticker,
            'Name': company.name,
            'ROA': company.roa_cy,
            'CFO': company.cfo,
            'dROA': company.dRoa,
            'Accrual': company.accrual,
            'dLeverage': company.dLeverage,
            'dLiquid': company.dLiquid,
            'EQ_Offered': company.eqOffered,
            'dMargin': company.dMargin,
            'dTurn': company.dTurn,
            'f_score': calcF_score(company)
        }
    
        formateData.append(info)
    df = pd.DataFrame(formateData)
    return df