from sklearn.linear_model import LogisticRegression
from BinaryDataProcessing import getTrainTestData
from EvaluateStrategy import evaluateStrategy
from sklearn.grid_search import GridSearchCV

# This script creates a Logistic Regressor which trains and predict the probability of a click
# It applies GridSearchCV in order to tune the 'C' parameter for the LR.
# It saves the results to logistic_pctr.csv file
# It evaluates the results and plot them the relation between the number of clicks and base_bid

def save_to_file(y_pred):
    csv = open('logistic_pctr.csv', "w")
    columnTitleRow = "bidprice\n"
    csv.write(columnTitleRow)

    for i in range(0, len(y_pred)):
        pred = y_pred[i]
        row = str(pred)+"\n"
        csv.write(row)
    csv.close()


# Get the training and testing data
X_train, y_train, X_test, y_test, features, dataset, test = getTrainTestData()


# Apply GridSearchCV in order to optimize the 'C' parameter for LR
logisticRegressor = LogisticRegression()
param_grid = {'C': [0.1, 1, 10, 0.001] }
classifier = GridSearchCV(estimator=logisticRegressor, cv=3, param_grid=param_grid, n_jobs=1)
classifier.fit(X_train, y_train)

best_logistic_regressor = classifier.best_estimator_

print("Best regressor:")
print(best_logistic_regressor)

# This is the expected optimized LR, uncomment to use directly and comment above GridSearchCV
# best_logistic_regressor = LogisticRegression(C=0.1, class_weight=None, dual=False, fit_intercept=True,
#          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
#          penalty='l2', random_state=None, solver='sag', tol=0.0001,
#          verbose=0, warm_start=False)

best_logistic_regressor.fit(X_train, y_train)

results = best_logistic_regressor.predict_proba(X_test)
y_pred = results[:, 1]

# save the result so it can be used by ORBTbidding
save_to_file(y_pred)

# Evaluate the strategy in terms of number of clicks, impressions, CTR, CPC, CPM, etc
# and it tunes the base_bid and plots the number of clicks vs base_bid
evaluateStrategy(y_pred)



