from sklearn.linear_model import Ridge
from DataProcessing import getTrainTestData
from EvaluateStrategy import evaluateStrategy
from sklearn.grid_search import GridSearchCV


# Get the training and testing data
X_train, y_train, X_test, y_test, c, v, d = getTrainTestData()

# Initialize regressor
ridgeReg = Ridge(normalize=True)
param_grid = {'alpha': [0.001, 0.01, 0.05, 0.1, 1]}
classifier = GridSearchCV(estimator=ridgeReg, cv=3, param_grid=param_grid, n_jobs=1)
classifier.fit(X_train, y_train)

best_logistic_regressor = classifier.best_estimator_
print("Best Estimator:")
print(best_logistic_regressor)

# This is the best estimator, uncomment to use and comment GridSearchCV
#best_logistic_regressor = Ridge(alpha=0.05, copy_X=True, fit_intercept=True, max_iter=None,
#   normalize=True, random_state=None, solver='auto', tol=0.001)
best_logistic_regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = best_logistic_regressor.predict(X_test)

# Evaluate the results
evaluateStrategy(y_pred)