from sklearn.neighbors import KNeighborsClassifier #importing the modle from sklearn
from sklearn.model_selection import train_test_split #importing a function to split the data
import pandas as pd
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import os
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

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

features_to_check = ["base","base_robust","all","novel","hybrid_robust"]

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

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)  # 75% training and 25% test
    # Create Decision Tree classifer object
    classifier = KNeighborsClassifier(n_neighbors=5)

    sc_x = StandardScaler()
    X_train = sc_x.fit_transform(X_train)
    X_test = sc_x.transform(X_test)

    mm_x = MinMaxScaler()
    X_train = mm_x.fit_transform(X_train)
    X_test = mm_x.transform(X_test)

    # Train Decision Tree Classifer
    classifier.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = classifier.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("f1 Score:", metrics.f1_score(y_test, y_pred, average='macro'))
    print("precision:", metrics.precision_score(y_test, y_pred, average='macro'))
    print("recall:", metrics.recall_score(y_test, y_pred, average='macro'))
