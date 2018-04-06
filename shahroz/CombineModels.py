from dataProcessing import *
from evaluateStrategy import *


usecols_lr = ['click', 'hour', 'weekday', 'region', 'advertiser', 'useragent', 'slotformat', 'slotvisibility',
           'adexchange', 'usertag'] #usertag
# Get the training and testing data

X_train, y_train, X_valid, y_valid, feat, dataset, validation = get_data(usecols_lr)

def writeOut(name, y_pred):
    import csv

    with open('/Users/shahrozahmed/Desktop/we_data/' + name, 'w', newline='') as f:
        thewriter = csv.writer(f)

        thewriter.writerow(['', 0])
        for i in range(y_pred.size):
            thewriter.writerow([i, y_pred[i]])

def gbc_y():
    from sklearn.ensemble import GradientBoostingClassifier
    regressor_gb = GradientBoostingClassifier()
    regressor_gb.fit(X_train, y_train)
    y_pred_gb = regressor_gb.predict_proba(X_valid)
    return y_pred_gb[:, 1]


gbc = gbc_y()
writeOut("GBc.csv", gbc)


def adaboost():
    print("1")
    from sklearn.ensemble import AdaBoostRegressor
    regressor = AdaBoostRegressor(base_estimator=None, n_estimators=250, learning_rate=0.001, loss='linear', random_state=None)
    regressor.fit(X_train, y_train)
    print("2")
    y_pred = regressor.predict(X_valid)
    return y_pred


ada = adaboost()
writeOut("adaboost.csv", ada)

def LR():
    print("3")
    from sklearn.linear_model import LogisticRegression
    regressor = LogisticRegression(penalty='l2', class_weight='balanced')
    regressor.fit(X_train, y_train)
    print("4")
    y_pred_lr = regressor.predict_proba(X_valid)
    return y_pred_lr[:, 1]

logr = LR()
writeOut("LogR.csv", logr)

def XGB():
    from xgboost import XGBClassifier
    model = XGBClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_valid)
    return y_pred


def LinR():
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    print("4")
    y_pred = regressor.predict(X_valid)
    return y_pred

linr = LinR()
writeOut("LinR.csv", linr)


def GridS():
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import GridSearchCV
    gb = GradientBoostingClassifier()
    model = GridSearchCV(estimator = gb)
    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_valid)
    return y_pred


gs = GridS()
writeOut("grids.csv", gs)


def Gbc():
    from sklearn.ensemble import GradientBoostingClassifier, AdaBoostRegressor
    from sklearn.linear_model import LogisticRegression
    from mlxtend.regressor import StackingRegressor
    from sklearn.svm import SVR
    adaboost = AdaBoostRegressor()
    lr = LogisticRegression
    gb = GradientBoostingClassifier()
    svr = SVR(kernel='linear')
    svr_rbf = SVR(kernel='rbf')
    regressors = [svr, adaboost, gb]
    stregr = StackingRegressor(regressors=regressors, meta_regressor=svr_rbf)
    stregr.fit(X_train, y_train)
    outpred = stregr.predict(X_valid)
    evaluate_strategy(outpred)

# merging adaboost and gradientboost
#pred_ad = adaboost()
#pred_gbc = gbc_y()
#print("1.1")
#out_pred = (pred_gbc + pred_ad)/2

