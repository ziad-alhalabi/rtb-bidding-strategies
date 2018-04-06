from dataProcessing import *
from evaluateStrategy import *
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

# Get the training and testing data


usecols = ['click', 'weekday', 'region', 'slotwidth', 'slotheight', 'advertiser', 'useragent', 'city', 'slotprice', 'slotformat']

# 'click', 'city', 'region', 'slotwidth', 'slotheight', 'useragent', 'slotprice', 'usertag', 'weekday',
          #     'advertiser', 'slotvisibility', 'domain'

X_train, y_train, X_valid, y_valid, feat, dataset, validation = get_data(usecols)

print("1")

regressor = GradientBoostingClassifier()

regressor.fit(X_train, y_train)
print("2")

y_pred_gb = regressor.predict_proba(X_valid)

y_pred = y_pred_gb[:, 1]

print("3")

visualise_auc(y_pred_gb, dataset, y_valid)


evaluate_strategy(y_pred)

# download pCTR
import csv
with open('/Users/shahrozahmed/Desktop/we_data/pCTR_gradient.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['', 0])
    for i in range(y_pred.size):
        thewriter.writerow([i, y_pred[i]])

# Evaluate the results


