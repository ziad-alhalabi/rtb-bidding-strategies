
from DataProcessing import getTestOriginalData
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# This is a helper function that evaluates a list of predicted CTRs
# by calculating the number of clicks, impressions, cost, CTR, CPC, and CPM.
# It loops over a range of base_bids in order to find the optimal one
# It plots the number of clicks verses the base_bid

def evaluateStrategy(y_pred):
    df = pd.DataFrame(columns=['bid', 'clicks', 'imps', 'spent', 'CTR', 'CPC', 'CPM'])
    lists = {'bid': [], 'clicks': [], 'imps': [], 'spent': [], 'ctr': [], 'cpc': [], 'cpm': []}

    budget = 6250000
    avgCTR = 0.000738
    maxClick = 0
    maxClickBaseBid = 0

    testOriginal = getTestOriginalData()
    testclicks = testOriginal.iloc[:, 0].values
    testpayprice = testOriginal.iloc[:, 21].values

    for baseBid in range(20, 250):
        cost = 0.0
        numClicked = 0
        numImpressions = 0

        for i in range(len(y_pred)):
            testclick = testclicks[i]
            clickProb = y_pred[i]
            testPayPrice = testpayprice[i]

            bid = (baseBid * clickProb) / avgCTR

            if bid > testPayPrice and (cost + testPayPrice <= budget):
                cost += testPayPrice

                numImpressions = numImpressions + 1
                numClicked = numClicked + testclick

            if cost >= budget:
                break

        spent = cost / 1000
        ctr = ((numClicked / numImpressions) * 100)
        cpm = ((spent / numImpressions) * 1000)
        cpc = (spent / numClicked)

        lists['bid'].append(baseBid)
        lists['clicks'].append(numClicked)
        lists['imps'].append(numImpressions)
        lists['spent'].append(spent)
        lists['ctr'].append(ctr)
        lists['cpc'].append(cpc)
        lists['cpm'].append(cpm)

        if numClicked>maxClick:
            maxClick = numClicked
            maxClickBaseBid = baseBid

    df.bid = lists['bid']
    df.clicks = lists['clicks']
    df.imps = lists['imps']
    df.spent = lists['spent']
    df.CTR = lists['ctr']
    df.CPC = lists['cpc']
    df.CPM = lists['cpm']

    print(df.iloc[np.where(df.clicks == df.clicks.max())[0]])

    print("maxClick %f" % maxClick)
    print("maxClickBaseBid %f" % maxClickBaseBid)

    #Visualize the results
    plt.plot(lists['bid'], lists['clicks'])
    plt.xlabel('baseBids')
    plt.ylabel('Number of clicks')
    plt.show()
