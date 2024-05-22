#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 12:59:25 2024

@author: muthyala.7
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.metrics import mean_squared_error,r2_score

fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}
import matplotlib
matplotlib.rc('font', **font)


'''
Specific Energy train and test plots..
'''

df_train = pd.read_csv('./Specific_Energy_train.csv')

df_test_100K = pd.read_csv('./Specific_Energy_test_file.csv')


plt.plot([0,3],[0,3],linestyle='--')

predicted_specific_energy = 1717.161781*(df_train['VR2_Dzare']/(df_train['VR2_Dzp']*(df_train['ATS1Z']+df_train['ATS2Z']))) + 0.02741337642
predicted_specific_energy_test =  1717.161781*(df_test_100K['VR2_Dzare']/(df_test_100K['VR2_Dzp']*(df_test_100K['ATS1Z']+df_test_100K['ATS2Z']))) + 0.02741337642

import math
r2 = r2_score(df_train.Redox,predicted_specific_energy)
rslt_meansqre_err = mean_squared_error(df_train.Redox,predicted_specific_energy)
root_meansqre_err= math.sqrt(rslt_meansqre_err)
plt.scatter(df_train.Redox,predicted_specific_energy,s=40,alpha=0.8,label=f'QDs - R$^2$:{r2:.3f}; RMSE:{round(root_meansqre_err,3)}')
plt.legend()
plt.xlabel('DFT Specific Energy values')
plt.ylabel('Predicted Specific Energy values')
plt.title('Paraquinone training pairity plot')
plt.show()

fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}
import matplotlib
matplotlib.rc('font', **font)
plt.plot([0,3],[0,3],linestyle='--')
r2 = r2_score(df_test_100K.Specific_Energy,predicted_specific_energy_test)
rslt_meansqre_err = mean_squared_error(df_test_100K.Specific_Energy,predicted_specific_energy_test)
root_meansqre_err= math.sqrt(rslt_meansqre_err)
plt.scatter(df_test_100K.Specific_Energy,predicted_specific_energy_test,s=40,alpha=0.8,label=f'QDs - R$^2$:{r2:.3f}; RMSE:{round(root_meansqre_err,3)}')
plt.legend()
plt.xlabel('DFT Specific Energy values')
plt.ylabel('Predicted Specific Energy values')
plt.title('Quinone Database testing pairity plot')
plt.show()


'''
Solvation Energy train and test plots...
'''

df_train_solv = pd.read_csv('./Solvation_Energy_train.csv')

df_test_solv = pd.read_csv('./solvation_energy_test_file.csv')

solv_predicted = -0.0008272568654*((df_train_solv.ATS1Z/df_train_solv.GATS2d)*(df_train_solv.MID_N+df_train_solv.GATS3p)) -0.09311602313
solv_predicted_test = -0.0008272568654*((df_test_solv.ATS1Z/df_test_solv.GATS2d)*(df_test_solv.MID_N+df_test_solv.GATS3p)) -0.09311602313

fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}
import matplotlib
matplotlib.rc('font', **font)
plt.plot([-6,0],[-6,0],linestyle='--')
r2 = r2_score(df_train_solv.Solvation,solv_predicted)
rslt_meansqre_err = mean_squared_error(df_train_solv.Solvation,solv_predicted)
root_meansqre_err= math.sqrt(rslt_meansqre_err)
plt.scatter(df_train_solv.Solvation,solv_predicted,s=40,alpha=0.8,label=f'QDs - R$^2$:{r2:.3f}; RMSE:{round(root_meansqre_err,3)}')
plt.legend()
plt.xlim(-4,0)
plt.ylim(-4,0)
plt.xlabel('DFT Solvation Energy values')
plt.ylabel('Predicted Solvation Energy values')
plt.title('Solvation Energy Training pairity plot')
plt.show()


fig = plt.figure(figsize=(10,8))
font = {'weight' : 'bold',
        'size'   : 22}
import matplotlib
matplotlib.rc('font', **font)
plt.plot([-6,0],[-6,0],linestyle='--')
r2 = r2_score(df_test_solv.Solvation_Energy,solv_predicted_test)
rslt_meansqre_err = mean_squared_error(df_test_solv.Solvation_Energy,solv_predicted_test)
root_meansqre_err= math.sqrt(rslt_meansqre_err)
plt.scatter(df_test_solv.Solvation_Energy,solv_predicted_test,s=40,alpha=0.8,label=f'QDs - R$^2$:{r2:.3f}; RMSE:{round(root_meansqre_err,3)}')
plt.legend()
plt.xlim(-4,0)
plt.ylim(-4,0)
plt.xlabel('DFT Solvation Energy values')
plt.ylabel('Predicted Solvation Energy values')
plt.title('Solvation Energy Testing pairity plot')
plt.show()
