import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from BinaryDataProcessing import getTrainTestData

# This class implements an optimized version of constant bidding
# A LogisticRegression is added to predict the probability of a click
# The strategy outputs a prediction if the probability is > 0.002
# The startegy is evaluated and a plot is displayed to show the
# number of clicks versus the different constant bids


def getProb():
    X_train, y_train, X_test, y_test, features, dataset, test = getTrainTestData()
    best_logistic_regressor = LogisticRegression(C=0.1, class_weight=None, dual=False, fit_intercept=True,
                                                 intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
                                                 penalty='l2', random_state=None, solver='sag', tol=0.0001,
                                                 verbose=0, warm_start=False)
    best_logistic_regressor.fit(X_train, y_train)

    y_pred_prob = best_logistic_regressor.predict_proba(X_test)
    return y_pred_prob[:, 1]

def main():
    budget = 6250000
    maxClick = 0
    numImpressions = 0
    numClicked = 0
    constants = []
    clicks = []
    constant = 0
    testClicks,	testPayPrices = getTestData()
    bestConstant = 0	
    bestCtr = 0
    bestCpm = 0
    bestCpc = 0
    y_pred = getProb()

    print(y_pred)
    for constant in range(1, 4):
        cost = 0.0
        numClicked = 0
        numImpressions = 0

        print(constant)

        for i in range(len(testClicks)):
            testClick = testClicks[i]
            
            testPayPrice = testPayPrices[i]
            bid = constant
            proba = y_pred[i]

            if (proba>0.002 and bid > testPayPrice and (cost + testPayPrice <= budget)):
                cost += testPayPrice
                numImpressions = numImpressions + 1
                numClicked = numClicked + testClick

            if (cost >= budget):
                break

        #evaluation points:
		# number of clicks, CTR, CPM, CPC
        if numImpressions>0:
            ctr = (float(numClicked)/numImpressions)*100 #to turn into percentage
            cpm = (cost/numImpressions)*1000
        if numClicked>0:
            cpc = cost/numClicked

        constants.append(constant)
        clicks.append(numClicked)
        if numClicked>maxClick:
            maxClick = numClicked
            bestConstant = constant
            bestCtr = ctr # assigning evaluators here ties evaluators to the constant which gets the most clicks,
            bestCpm = cpm # so it's not possible to see what was the constant which got the highest evaluator (e.g. CTR)
            bestCpc = cpc

    print("Most clicks achieved %f" % maxClick)
    print("Constant-bid which achieved most clicks %f" % bestConstant)
    print("ctr %f" % bestCtr)
    print("cpm %f" % bestCpm)
    print("cpc %f" % bestCpc)
    print("imps %f" % numImpressions)
    print("cost %f" % cost)

    #Visualize the results
    plt.plot(constants, clicks)
    plt.xlabel('constant bid')
    plt.ylabel('Number of clicks')
    plt.show()

def getTestData():
    VALIDATION_PATH = "validation.csv"
    testOriginal = pd.read_csv(VALIDATION_PATH)
    testclicks = testOriginal.iloc[:, 0].values
    testpayprice = testOriginal.iloc[:, 21].values
    return testclicks, testpayprice
	
if __name__ == "__main__":
    main()