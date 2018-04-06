from dataProcessing import *
from evaluateStrategy import *
import pandas as pd
import numpy as np


usecols_lr = ['click', 'city', 'region', 'slotwidth', 'slotheight', 'useragent', 'slotprice', 'usertag', 'weekday',
               'advertiser', 'slotvisibility', 'domain']
# Get the training and testing data
X_train, y_train, X_valid, y_valid, val_feat, dataset, validation = get_data(usecols_lr)

print("1")
from sklearn.linear_model import LogisticRegression
# penalty='l2', class_weight='balanced'
regressor = LogisticRegression()
print("2")

X_train = dataset[val_feat]

regressor.fit(X_train, y_train)
print("3")

y_pred_lr = regressor.predict_proba(X_valid)
y_pred = y_pred_lr[:, 1]

print("3")
# test_predict = regressor.fit(X_train, y_train).predict(X_test)
visualise_auc(y_pred_lr, dataset, y_valid)

evaluate_strategy(y_pred)

evaluate_strategy2(y_pred)

'''
usecols_rf = ['click', 'hour', 'weekday', 'region', 'advertiser', 'useragent', 'slotformat', 'slotvisibility',
              'adexchange', 'payprice', 'usertag']
# Get the training and testing data
X_train, y_train, X_valid, y_valid, feat, dataset, validation = get_data(usecols_rf)
print("1")


from sklearn.ensemble import RandomForestClassifier

rf_regressor = RandomForestClassifier(n_jobs = -1, n_estimators = 300, random_state =100,
                                      max_features = "auto", min_samples_leaf = 50, class_weight = "balanced")
rf_regressor.fit(X_train, y_train)
print("2")
y_pred_rf = rf_regressor.predict_proba(X_valid)
y_pred = y_pred_rf[:, 1]
evaluate_strategy(y_pred)

'''


