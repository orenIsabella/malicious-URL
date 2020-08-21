#!/usr/bin/env python

import itertools
import numpy as np
import pandas as pd
import os
import time
import random

from Models.ELM import ELMClassifier

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import pearsonr


features_check = {
	"base": {
		"features"     : [1,2,3,4,5,6,7,8,9],
		"C"            : 0.001,
		"n_hidden"     : 100,
		"y_column_idx" : 10,
		"feature_file" : "../Datasets/features_extractions/base_(all).csv"
	},
	"base_robust": {
		"features"     : [2,6,8,9],
		"C"            : 0.001,
		"n_hidden"     : 10,
		"y_column_idx" : 10,
		"feature_file" : "../Datasets/features_extractions/base_(all).csv"
	},
	"all": {
		"features"     : [1,2,3,4,5,6,7,8,9,10,11,13,15],
		"C"            : 50,
		"n_hidden"     : 150,
		"y_column_idx" : 17,
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	},
	"novel": {
		"features"     : [10,11,13,15],
		"C"            : 0.004,
		"n_hidden"     : 50,
		"y_column_idx" : 17,
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	},
	"hybrid_robust": {
		"features"     : [2,6,8,9,10,11,13,15],
		"C"            : 0.01,
		"n_hidden"     : 100,
		"y_column_idx" : 17,
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	},
    "PC": {
        "features"     : [10,11],
        "feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
    }
}

model_name        = "PC"
features_to_check = ["PC"]

##################################


threshold       = 0.5
learning_rate   = 0.001
n_splits		= 10
test_size		= 0.25

path               = os.path.dirname(os.path.abspath(__file__))
features_file_name = "../Datasets/features_extractions/median_9_2_(75-25)_vt_include.csv"
features_file      = os.path.join(path, features_file_name)

#for every variable in freatures_to_check (We have 5) we will check if we can find a malicious sign. if so we will append the url to df.
for features_set in features_to_check:
    print("\n\nChecking features - %s" % (features_set))
    features_file = os.path.join(path, features_check[features_set]["feature_file"])
    data = pd.read_csv(features_file)
    data.head()
    feature_cols = features_check[features_set]["features"]
    a = ["0"] * len(feature_cols)
    c = 0
    for f in feature_cols:
        a[c] = str(f)
        c = c+1
    #print(a)
    X = data[a] # Features
    y = data['0'] # Target variable

    corr, _ = pearsonr(data[a[0]], data[a[1]])
    print('Pearsons correlation: %.3f' % corr)
    # for a in data[a[0]]:
    #     print(a)


#print(X[0])