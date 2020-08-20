import numpy as np
from sklearn.ensemble import RandomForestClassifier

'''
This module provides functions to assist with analysis of our data
'''
def annotations_for_ARU(X_train, y_train, X_test):
  X_train = np.asarray(X_train)
  y_train = np.asarray(y_train)
  X_test = np.asarray(X_test)
  clf = RandomForestClassifier(random_state=0, n_estimators=100)
  clf.fit(X_train, y_train)
  y_predictions = clf.predict(X_test)
  return y_predictions