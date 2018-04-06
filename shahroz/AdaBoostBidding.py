from dataProcessing import *
from evaluateStrategy import *
import pandas as pd
import numpy as np


# Get the training and testing data
columns = ['click', 'city', 'region', 'slotwidth', 'slotheight', 'useragent', 'slotprice', 'usertag', 'weekday',
               'advertiser', 'slotvisibility', 'domain']




X_train, y_train, X_valid, y_valid, feat, dataset, validation = get_data(columns)

print("1")

from sklearn.ensemble import AdaBoostRegressor

# Initialize regressor - > 120
regressor = AdaBoostRegressor()

# AdaBoost Bidding

reg_fit = regressor.fit(X_train, y_train)
print("2")

features_selected = remove_features(feat, reg_fit)
X_train = dataset[features_selected]

# fit again accordingly
reg_fit = regressor.fit(X_train, y_train)
X_valid = validation[features_selected]
visualise_features(reg_fit, X_valid, features_selected)
y_pred = reg_fit.predict(X_valid)

#



# test_predict = regressor.fit(X_train, y_train).predict(X_test)

#visualise_auc(y_pred, dataset, y_valid)


evaluate_strategy(y_pred)


# download pCTR
import csv

with open('/Users/shahrozahmed/Desktop/we_data/pCTR_adaboost.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['', 0])
    for i in range(y_pred.size):
        thewriter.writerow([i, y_pred[i]])

pCTRval = pd.read_csv('/Users/shahrozahmed/Desktop/we_data/pCTR_adaboost.csv')
df_val = pd.read_csv('/Users/shahrozahmed/Desktop/we_data/validation.csv')




