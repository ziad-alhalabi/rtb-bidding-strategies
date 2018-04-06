from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from EvaluateStrategy import evaluateStrategy
from DataProcessing import getTrainTestData
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from math import sqrt

# This script creates and tests different combinations of model ensemlble based on:
# the three models: Linear Regression, Ridge Regression and GBRT

X_train, y_train, X_test, y_test, features, dataset, test = getTrainTestData()

# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_y_pred = lr.predict(X_test)
rms_linear = sqrt(mean_squared_error(y_test, lr_y_pred))
print("Linear regression RMSE= %f" % rms_linear)

# Ridge Regression
ridgeReg = Ridge(alpha=0.05, normalize=True)
ridgeReg.fit(X_train, y_train)
rigde_y_pred = ridgeReg.predict(X_test)
rms_ridge = sqrt(mean_squared_error(y_test, rigde_y_pred))
print("Ridge regression RMSE= %f" % rms_ridge)

# GBRT
meta_regressor = GradientBoostingRegressor(alpha=0.9, criterion='friedman_mse', init=None,
             learning_rate=0.1, loss='ls', max_depth=10, max_features=1.0,
             max_leaf_nodes=None, min_impurity_decrease=0.0,
             min_impurity_split=None, min_samples_leaf=10,
             min_samples_split=2, min_weight_fraction_leaf=0.0,
             n_estimators=50, presort='auto', random_state=None,
             subsample=1.0, verbose=0, warm_start=False)
meta_regressor.fit(X_train, y_train)
gbrt_y_pred = meta_regressor.predict(X_test)
rms_gbrt = sqrt(mean_squared_error(y_test, gbrt_y_pred))
print("GBRT RMSE= %f" % rms_gbrt)


# Testing different coefficients
def try_coeff(c1, c2, c3):
    print ("Testing c1= %f" % c1)
    print ("Testing c2= %f" % c2)
    print ("Testing c3= %f" % c3)
    new_pred = []
    for i in range(len(gbrt_y_pred)):
        pred = (c1 * gbrt_y_pred[i]) + (c2 * rigde_y_pred[i]) + (c2 * lr_y_pred[i])
        new_pred.append(pred)

    evaluateStrategy(new_pred)


try_coeff(0.33, 0.33, 0.33)
try_coeff(0.5, 0.25, 0.25)
try_coeff(0.6, 0.2, 0.2)
try_coeff(0.7, 0.15, 0.15)
try_coeff(0.8, 0.1, 0.1)
try_coeff(0.9, 0.05, 0.05)