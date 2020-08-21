#!/usr/bin/env python

##############################################
# Author: Nitay Hason
# SVM class
##############################################

import numpy as np
import matplotlib.pyplot as plt
import time

from sklearn import svm
from sklearn import metrics

from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

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

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

class SVM:
	def __init__(self, df, degree=3, kfolds=10, test_size=0.25, C=100, gamma=0.00035, threshold=0.5, drop_columns=[]):
		self.df              = df
		self.degree          = degree
		self.kfolds          = kfolds
		self.test_size       = test_size
		self.C               = C
		self.gamma           = gamma
		self.drop_columns    = drop_columns
		self.threshold		 = threshold
		self.X	             = None
		self.y               = None
		self.X_train         = None
		self.X_test          = None
		self.y_train         = None
		self.y_test          = None
		self.idx_train       = None
		self.idx_test        = None
		self.model 			 = None
		self.model_history	 = None

	"""build the dataset without unwanted columns, normalize them and add the features and labels to it"""
	def build(self, verbose=1):
		use_dataset = self.df.copy()
		# Drop unwanted columns
		if len(self.drop_columns)>0:
			use_dataset = np.delete(self.df, self.drop_columns, 1)
		use_dataset = np.asfarray(use_dataset,np.dtype('Float64'))

		# Normlize the dataset
		self.scaler= MinMaxScaler().fit(use_dataset[:, :-1])
		dataset_norm = self.scaler.transform(use_dataset[:, :-1])
		# Split into features and labels
		self.X, self.y = dataset_norm, np.transpose([use_dataset[:, -1]]).ravel()

		if self.degree > 1:
			polynomial_features= PolynomialFeatures(degree=self.degree, include_bias=False)
			self.X = polynomial_features.fit_transform(self.X)

	"""train the given data- first split the data to train and test, then take the train data according to the model, and lastly print the accuracy, percision and loss. """
	def train(self, optimizer=0, kernel='rbf', verbose=0):
		# Split the data to train and test
		indices = np.arange(self.y.shape[0])
		self.X_train, self.X_test, self.y_train, self.y_test, self.idx_train, self.idx_test = train_test_split(self.X, self.y, indices, stratify=self.y, test_size=self.test_size, random_state=42)

		# sc_x = StandardScaler()
		# self.X_train = sc_x.fit_transform(self.X_train)
		# self.X_test = sc_x.transform(self.X_test)
		#
		# mm_x = MinMaxScaler()
		# self.X_train = mm_x.fit_transform(self.X_train)
		# self.X_test = mm_x.transform(self.X_test)

		kf = KFold(n_splits=self.kfolds, random_state=None, shuffle=False)
		kf.get_n_splits(self.X)

		start      = time.time()
		self.model = svm.SVC(gamma=self.gamma, C=self.C, kernel=kernel, probability=True)

		for train_index, test_index in kf.split(self.idx_train):
			X_train_fold, X_test_fold = self.X_train[train_index], self.X_train[test_index]
			y_train_fold, y_test_fold = self.y_train[train_index], self.y_train[test_index]

			self.model.fit(X_train_fold,y_train_fold)

			if verbose>0:
				y_pred    = self.model.predict(X_test_fold)
				accuracy  = accuracy_score(y_test_fold, y_pred)
				precision = precision_score(y_test_fold, y_pred)
				loss      = log_loss(y_test_fold, y_pred)

				print("Accuracy {}, Precision {}, Loss {}".format(accuracy,precision,loss))

		end   = time.time()
		print("\nTraining time:")
		print(end - start)

	"""after training its time to predict the outcomes and precision"""
	def predict(self, verbose=1):
		y_pred       = self.model.predict(self.X_test)
		# predict probabilities for test set
		y_pred_proba = self.model.predict_proba(self.X_test)[::,1]

		y_pred = y_pred_proba.copy()
		y_pred[y_pred>=self.threshold]=np.float64(1)
		y_pred[y_pred<self.threshold]=np.float64(0)

		FPR, TPR, _  = roc_curve(self.y_test, y_pred_proba)
		AUC          = auc(FPR, TPR)

		# accuracy: (tp + tn) / (p + n)
		accuracy    = accuracy_score(self.y_test, y_pred)
		# precision tp / (tp + fp)
		precision   = precision_score(self.y_test, y_pred)
		# recall: tp / (tp + fn)
		recall      = recall_score(self.y_test, y_pred)
		# f1: 2 tp / (2 tp + fp + fn)
		f1          = f1_score(self.y_test, y_pred)
		#loss
		loss        = log_loss(self.y_test, y_pred)
		# kappa
		kappa       = cohen_kappa_score(self.y_test, y_pred)
		# ROC AUC
		auc_score   = roc_auc_score(self.y_test, y_pred_proba)
		# Confusion matrix
		matrix      = confusion_matrix(self.y_test, y_pred)
		# Classification report
		cr          = classification_report(self.y_test,y_pred,digits=3)

		return_dict = {"accuracy":accuracy,"precision":precision,"recall":recall,"f1":f1,"loss":loss,"kappa":kappa,"auc":auc_score,"confusion_matrix":matrix,"classification_report":cr}

		if verbose>0:
			print('Accuracy: %f' % accuracy)
			print('Precision: %f' % precision)
			print('Recall: %f' % recall)
			print('F1 score: %f' % f1)
			print('Loss: %f' % loss)
			print('Cohens kappa: %f' % kappa)
			print('ROC AUC: %f' % auc_score)
			print(matrix)
			print(cr)

		return return_dict
