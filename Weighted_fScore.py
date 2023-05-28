#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:48:20 2023

@author: ishratvasid
"""
from tqdm import tqdm
import numpy as np
from sklearn.linear_model import Lasso
import pandas as pd
import os
os.chdir("/Users/ishratvasid/Desktop/GitHub/WQU-Capstone---Piotroski-F-Score-Analysis/")
yourapikey = 'a9825b793634b1fd7b14ed94547c0849'

from getPriceReturn import getAPIPriceReturn
from fscore import calcWeightedF_Score

output = pd.DataFrame(columns=['Year','Port1_Ret','Port1_Std','Port1_SR','Port2_Ret','Port2_Std','Port2_SR'])
for i in range(2010,2023):
    year = str(i)
    data = pd.read_excel("Data/FScore_"+year+".xlsx")
    
    # Prepare your data
    X = data.iloc[:,2:11] # Independent variables
    Y = data.iloc[:,-1]  # Dependent variable
    
    # Create an instance of Lasso regression
    lasso = Lasso(alpha=0.1)  # Set the regularization parameter alpha
    
    # Fit the Lasso regression model
    lasso.fit(X, Y)
    coefficients = lasso.coef_
    
    data = calcWeightedF_Score(data, coefficients)
    
    #Backtesting
    startdate = year+'-01-01'     
    enddate = year+'-12-31' 
    
    ## Weighted FScore Strategy
    portfolio_1 = data.sort_values(['wFScore','Price_Ret'],ascending=False, ignore_index = True )
    portfolio_1.loc[0:120, 'Signal'] = 1
    #portfolio_1.loc[portfolio_1.index[-60:],'Signal'] = -1
    portfolio_1 = portfolio_1[~portfolio_1['Signal'].isna()][['Ticker','Signal']].reset_index(drop=True)
    for i in tqdm(range(len(portfolio_1))):
        ticker = portfolio_1.loc[i,'Ticker']
        print(i,' --- ', ticker)
        stock_ret = getAPIPriceReturn(ticker, startdate, enddate, yourapikey)
        portfolio_1.loc[i,'Price_Ret_t+1'] = stock_ret
    
    portfolio_1 = portfolio_1[~portfolio_1['Price_Ret_t+1'].isna()]
    #portfolio_1 =  pd.concat([portfolio_1.head(50), portfolio_1.tail(50)], ignore_index=True)
    portfolio_1 =  portfolio_1.head(100)
    portfolio1_tot_ret = np.nansum(portfolio_1['Price_Ret_t+1']*portfolio_1['Signal'])
    weights = np.ones(len(portfolio_1)) / len(portfolio_1)  # Equal weights for each stock
    portfolio1_std = np.sqrt(np.dot(weights.T, np.dot(np.cov(portfolio_1['Price_Ret_t+1']), weights)))
    portfolio1_SR = portfolio1_tot_ret/portfolio1_std
    
    ## Original FScore Strategy
    portfolio_2 = data.sort_values(['f_score','Price_Ret'],ascending=False, ignore_index = True )
    portfolio_2.loc[0:120, 'Signal'] = 1
    #portfolio_2.loc[portfolio_2.index[-60:],'Signal'] = -1
    portfolio_2 = portfolio_2[~portfolio_2['Signal'].isna()][['Ticker','Signal']].reset_index(drop=True)
    
    for i in tqdm(range(len(portfolio_2))):
        ticker = portfolio_2.loc[i,'Ticker']
        print(i,' --- ', ticker)
        stock_ret = getAPIPriceReturn(ticker, startdate, enddate, yourapikey)
        portfolio_2.loc[i,'Price_Ret_t+1'] = stock_ret
    
    portfolio_2 = portfolio_2[~portfolio_2['Price_Ret_t+1'].isna()]
   # portfolio_2 =  pd.concat([portfolio_2.head(50), portfolio_2.tail(50)], ignore_index=True)
    portfolio_2 =  portfolio_2.head(100)
    portfolio2_tot_ret = np.nansum(portfolio_2['Price_Ret_t+1']*portfolio_2['Signal'])
    weights = np.ones(len(portfolio_2)) / len(portfolio_2)  # Equal weights for each stock
    portfolio2_std = np.sqrt(np.dot(weights.T, np.dot(np.cov(portfolio_2['Price_Ret_t+1']), weights)))
    portfolio2_SR = portfolio2_tot_ret/portfolio2_std
    
    output.loc[len(output)] = [year, portfolio1_tot_ret, portfolio1_std, portfolio1_SR, portfolio2_tot_ret, portfolio2_std, portfolio2_SR]