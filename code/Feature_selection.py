#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 16:08:38 2023

@author: muthyala.7
"""

import pandas as pd 
import shutil
import os


'''
Read the datafile of the specific energy and the solvation energy for which we want to do the univariate feature selection with SISSO..
'''
df = pd.read_csv("path of the file for which we want to do univariate feature selection with SISSO..")

df.drop(df.columns[[0]],axis=1,inplace=True) # Dropping the index column..

'''
Create the individual datafolders that is used for the input and output datafiles..
'''

os.mkdir("path of folder creation..")
os.chdir("path of the folder created..")

'''
Loop for the entire mordred descriptors space to capture the metrics and non-linear relationships of the feature variable with target variable..
'''

for i in range('Insert the range of feature columns..'):
    individual_feature = df[df.columns[i]]
    
    #individual_feature.to_csv("individual_feature.csv") # Use if we want to save the individual feature datafiles..
    individual_feature.reset_index(drop=True,inplace=True)
    individual_feature.insert(0,'Index',individual_feature.index)
    
    individual_feature['Target_Property'] = df['Target_property']

    # Create the naming convention as per the SISSO.
    name = "train.dat"
    name2 = "predict.dat"
    
    #create the individual folder to perform the SISSO
    path1 = "./"+str(i)
    os.mkdir(path1)
    os.chdir(path1)
    
    #Take the input file and modify according to the datafile we have..
    src="/home/muthyala.7/SISSO_Toy_Examples/SISSO.in"  #Can be extraced from the SISSO github reository..
    file = open(src)
    shutil.copy(src,path1)
    path_IN_file = path1+"/SISSO.in"
    SISSO_in_file = open (path_IN_file,"r")
    SISSO_IN_File_Contents = SISSO_in_file.readlines()

    SISSO_IN_File_Contents[11] = "nsample=115 !(R) Number of samples in train.dat. For MTL, set nsample=N1,N2,... for each task. \n" #This line looks for the number of datapoints.. 
    SISSO_IN_File_Contents[10] = "desc_dim=1 !(R&C) Dimension of the descriptor, a hyperparmaeter. \n" #This linek looks for the number of dimensional equations we want to generate..
    SISSO_IN_File_Contents[20] = "nsf=1 !(R&C) Number of scalar features provided in the file train.dat  \n" #THis line looks for the number of feature variables in the datafile we are giving.
    SISSO_IN_File_Contents[21] = "ops='(+)(-)(*)(/)(exp)(sqrt)(log)(^2)' !(R&C) Please customize the operators from the list shown above. \n" #Defines the mathematical operator set with which we want to perform the featue expansion.. 
    
    '''
    '(+)(-)(*)(/)(^-1)(^2)(sqrt)(log)(exp)' - used for solvation energy..
    '(+)(-)(*)(/)(exp)(exp-)(^-1)(^2)(sqrt)(log)' - used for specific energy..
    '''
    
    with open (path_IN_file,"w") as file1:
        file1.writelines(SISSO_IN_File_Contents)
    individual_feature.to_csv(name,sep='\t',index=False) #Converting the data into required formati for SISSO..
   
    os.system("ulimit -s unlimited") #Freeing up space to run the SISSO..
    os.system("SISSO>log")# SISSO Execution


'''
Extract the RMSE of the features and create a dataframe for the feature variables with their RMSE
'''

RMSE1D =[]
feature_name =[]

for i in range ('Length of the feature variables..'):
    path = path1+str(i)
    os.chdir(path)
    path_out = path+"/SISSO.out"

    SISSO_Out = open (path_out,"r")

    SISSO_out_contents = SISSO_Out.readlines()
    
    Search_Keyword = "@@@descriptor: \n"
    index_pos = SISSO_out_contents.index(Search_Keyword)
    
    RMSE_1D = SISSO_out_contents[index_pos-1]
    RMSE_1D1 = RMSE_1D.split(" ")
    RMSE1D.append(RMSE_1D1[5])

    feature_name.append(df.columns[i])

data={'Feature Name':feature_name,'RMSE 1D':RMSE1D}
df_metrics=pd.DataFrame(data)



'''
Extract the features based on the top features with lower RMSE....
'''
df_metrics = df_metrics.sort_values(by='RMSE',ascendig = True)

df_train = df.loc[:,df_metrics['Feature Name'][:99]]   # This datafile is used for training the model with the SISSO framework..
