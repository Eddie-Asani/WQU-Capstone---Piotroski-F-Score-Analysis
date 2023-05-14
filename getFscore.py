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
        roa, cfo, droa, accrual, dlever, dLiquid, eqOffered, dMargin, dTurn, fScore = calcF_score(company)
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
            'ROA_Score': roa,
            'CFO_Score': cfo,
            'dROA_Score': droa,
            'Accrual_Score': accrual,
            'dLeverage_Score': dlever,
            'dLiquid_Score': dLiquid,
            'EQ_Offered_Score': eqOffered,
            'dMargin_Score': dMargin,
            'dTurn_Score': dTurn,
            'f_score': fScore
        }
    
        formateData.append(info)
    df = pd.DataFrame(formateData)
    return df