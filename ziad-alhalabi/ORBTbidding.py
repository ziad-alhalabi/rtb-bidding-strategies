
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# This script computes the ORTB using both LR and GBRT models results for pCTR
# It retrieves the results from logistic_pctr_val.csv and orbt_pctr.csv files
# LogisticRegressionBidding.py and GBRTBidding.py should be ran first so that these files exist
# It applies both ORTB formulas and evaluate and plot the results

LAMBDA = 5.2e-7

# ORBT Formula 1 is:
#       bid = sqrt((c/lambda) * pCTR) + c^2)  -  c
#           where c is a constant that we try to tune
#           lambda is Lagrangian multiplier, lambda = 5.2 * 10^-7
#           pCTR is the predicted CTR
def calculate_bid_formula1(y_pred, c):
    bids = []
    for pCTR in y_pred:
        bid = np.sqrt(((c/LAMBDA)*pCTR) + c*c) - c
        bids.append(bid)

    return bids


# ORBT Formula 2 is:
#       bid = c * (term^(1/3) - (1/term)^(1/3))
#           where term = (pCTR + sqrt(c^2 * lambda^2 + pCTR^2)) / (c * lambda)
#           where c is a constant that we try to tune
#           lambda is Lagrangian multiplier, lambda = 5.2 * 10^-7
#           pCTR is the predicted CTR
def calculate_bid_formula2(y_pred, c):
    bids = []
    for pCTR in y_pred:
        term = (pCTR + np.sqrt(c * c * LAMBDA * LAMBDA + pCTR * pCTR)) / (c * LAMBDA)
        bid = c * (term**(1/3) - (1.0/term)**(1/3))
        bids.append(bid)

    return bids


# This function evaluates an ORTB strategy and calculate CTR, CPC, CPM, etc
# The argument 'formula_type' indicates which ORTB formula to apply
# When formula_type == 2, it applies formula 2, else formula 1
def ortb_evaluate_strategy(y_pred, c, formula_type):
    df = pd.DataFrame(columns=['clicks', 'imps', 'spent', 'CTR', 'CPC', 'CPM'])
    lists = {'clicks': [], 'imps': [], 'spent': [], 'ctr': [], 'cpc': [], 'cpm': []}
    budget = 6250000
    numImpressions = 0
    numClicked = 0
    cost = 0

    if formula_type == 2:
        bids = calculate_bid_formula2(y_pred, c)
    else:
        bids = calculate_bid_formula1(y_pred, c)

    testOriginal = pd.read_csv("validation.csv")
    testclicks = testOriginal.iloc[:, 0].values
    testpayprice = testOriginal.iloc[:, 21].values

    for i in range(len(bids)):

        testclick = testclicks[i]
        testPayPrice = testpayprice[i]

        bid = bids[i]
        if (bid > testPayPrice and (cost + testPayPrice <= budget)):
            cost += testPayPrice
            numImpressions = numImpressions + 1
            numClicked = numClicked + testclick

        if cost >= budget:
            break

    spent = cost / 1000
    ctr = ((numClicked / numImpressions) * 100)
    cpm = ((spent / numImpressions) * 1000)
    cpc = (spent / numClicked)

    lists['clicks'].append(numClicked)
    lists['imps'].append(numImpressions)
    lists['spent'].append(spent)
    lists['ctr'].append(ctr)
    lists['cpc'].append(cpc)
    lists['cpm'].append(cpm)

    df.clicks = lists['clicks']
    df.imps = lists['imps']
    df.spent = lists['spent']
    df.CTR = lists['ctr']
    df.CPC = lists['cpc']
    df.CPM = lists['cpm']

    return df


def apply_both_formulas(y_pred):
    # Using Formula 1
    lists = {'clicks': [], 'c': []}
    maxdf = []
    maxC = 0
    maxClick = 0
    for c in range(1, 5):
        df = ortb_evaluate_strategy(y_pred, c, 1)
        click = df.clicks.max()
        lists['c'].append(c)
        lists['clicks'].append(click)

        if click > maxClick:
            maxClick = click
            maxC = c
            maxdf = df

    print("Formula1: maxClick %f" % maxClick)
    print("Formula1: maxC %f" % maxC)
    print(maxdf)

    # Using Formula 2
    lists2 = {'clicks': [], 'c': []}
    maxdf2 = []
    maxC2 = 0
    maxClick2 = 0
    for c in range(1, 5):
        df = ortb_evaluate_strategy(y_pred, c, 2)
        click = df.clicks.max()
        lists2['c'].append(c)
        lists2['clicks'].append(click)

        if click > maxClick2:
            maxClick2 = click
            maxC2 = c
            maxdf2 = df

    print("Formula2: maxClick %f" % maxClick2)
    print("Formula2: maxC %f" % maxC2)
    print(maxdf2)

    return lists, lists2


print("Testing LR")
lr_dataset = pd.read_csv('logistic_pctr_val.csv')
y_pred = lr_dataset['bidprice']
list_lr_f1, list_lr_f2 = apply_both_formulas(y_pred)

print("Testing GBRT")
gbrt_dataset = pd.read_csv('orbt_pctr.csv')
y_pred = gbrt_dataset['bidprice']
list_gbrt_f1, lists_gbrt_f2 = apply_both_formulas(y_pred)


# Visualizing the number of clicks vs c
plt.plot(list_lr_f1['c'], list_lr_f1['clicks'], label="NonLinear-LR-f1")
plt.plot(list_lr_f2['c'], list_lr_f2['clicks'], color='tab:orange', label="NonLinear-LR-f2")
plt.plot(list_gbrt_f1['c'], list_gbrt_f1['clicks'], color='tab:red', label="NonLinear-GBRT-f1")
plt.plot(lists_gbrt_f2['c'], lists_gbrt_f2['clicks'], color='tab:green', label="NonLinear-GBRT-f2")
plt.xlabel('c')
plt.ylabel('Number of clicks')
plt.legend()
plt.show()