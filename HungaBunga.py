import random
import os
from hunga_bunga import HungaBungaClassifier, HungaBungaRegressor, HungaBungaZeroKnowledge
from hunga_bunga.regression import gen_reg_data
from sklearn import datasets
import pandas as pd


# ---------- Getting The Data ----------
from sklearn.model_selection import train_test_split

features_check = {
	"base": {
		"features"     : [1,2,3,4,5,6,7,8,9],
		"feature_file" : "../Datasets/features_extractions/base_(all).csv"
	},
	"base_robust": {
		"features"     : [2,6,8,9],
		"feature_file" : "../Datasets/features_extractions/base_(all).csv"
	},
	"all": {
		"features"     : [1,2,3,4,5,6,7,8,9,10,11,13,15],
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	},
	"novel": {
		"features"     : [10,11,13,15],
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	},
	"hybrid_robust": {
		"features"     : [2,6,8,9,10,11,13,15],
		"feature_file" : "../Datasets/features_extractions/median_9_2_(25-75)_vt_include.csv"
	}
}

features_to_check = ["base"]

path               = os.path.dirname(os.path.abspath(__file__))
features_file_name = "../Datasets/features_extractions/median_9_2_(75-25)_vt_include.csv"
features_file      = os.path.join(path, features_file_name)

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

	# Split dataset into training set and test set
	X_c, X_r, y_c, y_r = train_test_split(X, y, test_size=0.25, random_state=1)  # 75% training and 25% test

	# iris = datasets.load_iris()
	# X_c, y_c = iris.data, iris.target
	# X_r, y_r = gen_reg_data(10, 3, 100, 3, sum, 0.3)

	# ---------- Classification ----------

	clf = HungaBungaClassifier()

	clf.fit(X_c, y_c)

	print(clf.predict(X_c))



	# ---------- Regression ----------

	# mdl = HungaBungaRegressor()
	# mdl.fit(X_r, y_r)
	# print(mdl.predict(X_c))



	# ---------- Zero Knowledge ----------

	# X, y = random.choice(((X_c, y_c), (X_r, y_r)))
	# mdl = HungaBungaZeroKnowledge()
	# mdl.fit(X, y)
	# print(mdl.predict(X), mdl.problem_type)