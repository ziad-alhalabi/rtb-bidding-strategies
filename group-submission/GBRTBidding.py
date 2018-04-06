from sklearn.ensemble import GradientBoostingRegressor
from sklearn.grid_search import GridSearchCV

from DataProcessing import getTrainTestData
from EvaluateStrategy import evaluateStrategy


# This script creates an GBRT which trains and predict the probability of a click
# It applies GridSearchCV in order to tune the different parameter for the GBRT.
# It saves the results to orbt_pctr.csv file
# It evaluates the results and plot them the relation between the number of clicks and base_bid

def save_to_file(y_pred):
    csv = open('orbt_pctr.csv', "w")
    columnTitleRow = "bidprice\n"
    csv.write(columnTitleRow)

    for i in range(0, len(y_pred)):
        pred = y_pred[i]
        row = str(pred)+"\n"
        csv.write(row)
    csv.close()


# Get the training and testing data
X_train, y_train, X_test, y_test, features, dataset, test = getTrainTestData()


param_grid={'n_estimators':[50, 100],
'learning_rate': [0.05, 0.1],
'max_depth':[5, 10],
'min_samples_leaf':[3, 5, 10],
'max_features':[1.0]
}


def gradient_booster(param_grid):
    estimator = GradientBoostingRegressor()
    classifier = GridSearchCV(estimator=estimator, cv=3, param_grid=param_grid, n_jobs=4)
    classifier.fit(X_train, y_train)
    print ("Best Estimator learned through GridSearch")
    print (classifier.best_estimator_)
    return classifier.best_estimator_


best_est = gradient_booster(param_grid)
print ("Best Estimator:")
print(best_est)

# This is the expected optimized LR, uncomment to use directly and comment above GridSearchCV
# best_est = GradientBoostingRegressor(alpha=0.9, criterion='friedman_mse', init=None,
#             learning_rate=0.1, loss='ls', max_depth=10, max_features=1.0,
#             max_leaf_nodes=None, min_impurity_decrease=0.0,
#             min_impurity_split=None, min_samples_leaf=10,
#             min_samples_split=2, min_weight_fraction_leaf=0.0,
#             n_estimators=50, presort='auto', random_state=None,
#             subsample=1.0, verbose=0, warm_start=False)

best_est.fit(X_train, y_train)
y_pred = best_est.predict(X_test)

# save the result so it can be used by ORBTbidding
save_to_file(y_pred)

# Evaluate the strategy in terms of number of clicks, impressions, CTR, CPC, CPM, etc
# and it tunes the base_bid and plots the number of clicks vs base_bid
evaluateStrategy(y_pred)

