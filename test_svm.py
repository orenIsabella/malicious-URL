#!/usr/bin/env python
import numpy as np
import pandas as pd
import sys, os
import time
import random

from Models.SVM import SVM

# Support-Vector Machine (SVM):
#  is a learning algorithm that constructs a high dimensional hyperplane used 
# to solve the classification and regression problem. Given a set of training examples, and their associated 
# labels, the algorithm trains a model that assigns new examples to one label or the other, making it a 
# nonprobabilistic binary linear classifier. In addition to performing linear classification, SVMs can efficiently 
# perform a non-linear classification using a kernel trick implicitly mapping their inputs into high-dimensional 
# feature spaces. A radial basis function (RBF) is a function that assigns a real value to each input from its 
# domain, and the value produced by the RBF is always an absolute value. 


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

model_name        = "svm"
features_to_check = ["base","base_robust","all","novel","hybrid_robust"]


threshold        = 0.5
degree           = 3
n_splits		 = 10
coef             = 100
gamma            = 2
test_size		 = 0.25

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
# create, build, train and predict the svm
	svm = SVM(new_df, degree=degree, threshold=threshold, kfolds=n_splits, test_size=test_size, C=coef, gamma=gamma)
	svm.build()
	svm.train()
	svm.predict()
