#!/usr/bin/env python
import numpy as np
import pandas as pd
import os
import time
import random

from Models.LogisticRegression import LogisticRegression

# Logistic Regression (LR):
# is a method for analyzing a dataset in which there are one or more independent 
# variables that determine an outcome. In logistic regression, the outcome is a binary dependent variable, i.e. 
# it only contains data coded as 1 (TRUE, malicious) or 0 (FALSE, benign). 


#features_check will contain 5 variables that will help us determine if the url is malicious or not.
features_check = {
	"base": {
		"features"	   : [1,2,3,4,5,6,7,8,9],
		"y_column_idx" : 10,
		"feature_file" : "../Datasets/features_extractions/base_(all).csv"
	},
	"base_robust": {
		"features": [2,6,8,9],
		"y_column_idx" : 10,
		"feature_file" : "../Datasets/features_extractions/base_(all).csv"
	},
	"all": {
		"features": [1,2,3,4,5,6,7,8,9,10,11,13,15],
		"y_column_idx" : 17,
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	},
	"novel": {
		"features": [10,11,13,15],
		"y_column_idx" : 17,
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	},
	"hybrid_robust": {
		"features": [2,6,8,9,10,11,13,15],
		"y_column_idx" : 17,
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	}
}

model_name        = "lr"
features_to_check = ["base","base_robust","all","novel","hybrid_robust"]


threshold       = 0.5
degree          = 3
n_splits		= 10
test_size		= 0.25

path               = os.path.dirname(os.path.abspath(__file__))

#for every variable in freatures_to_check (We have 5) we will check if we can find a malicious sign. if so we will append the url to df.
for features_set in features_to_check:
	print("\n\nChecking features - %s" % (features_set))
	features_file = os.path.join(path, features_check[features_set]["feature_file"])
	y_column_idx  = features_check[features_set]["y_column_idx"]
	start         = time.time()
	df            = pd.read_csv(features_file)
	######## Append artificial data by number of consecutive characters feature ########
	if 2 in features_check[features_set]["features"]:
		mal         = df[df[df.columns[y_column_idx]]==1].sample(500).copy()
		mal["2"]    = mal["2"].apply(lambda x:x*random.randint(3,9))
		df = df.append(mal, ignore_index=True)
	######################################## END #######################################
	use_columns   = features_check[features_set]["features"]
	use_columns.append(y_column_idx)

	new_df = df[df.columns[use_columns]]
	new_df = np.array(new_df.values)
	
	#Here is the important part of the test class.
	#we are building the lr, training it and trying to predict if a url is malicious.
	
	lr = LogisticRegression(new_df, degree=degree, threshold=threshold, kfolds=n_splits, test_size=test_size)
	lr.build()
	lr.train()
	lr.predict()
	end   = time.time()
	print("\nTraining time:")
	print(end - start)
