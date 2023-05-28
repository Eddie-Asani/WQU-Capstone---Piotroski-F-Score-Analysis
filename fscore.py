#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:06:26 2023

@author: ishratvasid
"""


def calcF_score(company):
    roa = 1 if company.roa_cy > 0 else 0
    cfo = 1 if company.cfo > 0 else 0
    droa = 1 if (company.roa_cy - company.roa_py) > 0 else 0
    accrual = 1 if company.cfo > company.roa_cy else 0
    dlever = 1 if company.dLeverage < 0 else 0
    dLiquid = 1 if company.dLiquid > 0 else 0
    eqOffered = 1 if company.eqOffered <= 0 else 0
    dMargin = 1 if company.dMargin > 0 else 0
    dTurn = 1 if company.dTurn > 0 else 0
    fScore = roa + cfo + droa + accrual + dlever + dLiquid + eqOffered + dMargin + dTurn
    
    return roa, cfo, droa, accrual, dlever, dLiquid, eqOffered, dMargin, dTurn, fScore

def calcWeightedF_Score(data, coefficients):
    wROA = data['ROA_Score'] * coefficients[0]
    wCFO = data['CFO_Score'] * coefficients[1]
    wdROA = data['dROA_Score'] * coefficients[2]
    wAccrual = data['Accrual_Score'] * coefficients[3]
    wdLeverage = data['dLeverage_Score'] * coefficients[4]
    wdLiquid = data['dLiquid_Score'] * coefficients[5]
    wEQ_Offered = data['EQ_Offered_Score'] * coefficients[6]
    wdMargin = data['dMargin_Score'] * coefficients[7]
    wdTurn = data['dTurn_Score'] * coefficients[8]
    data['wFScore'] = wROA + wCFO + wdROA + wAccrual + wdLeverage + wdLiquid + wEQ_Offered + wdMargin + wdTurn
    
    return data