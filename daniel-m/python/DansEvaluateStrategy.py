from DansDataProcessing import getTestOriginalData
import matplotlib.pyplot as plt
from fractions import Fraction
import numpy as np
import math

def ortb_evaluateStrategy(preds,ortb_ver):
    budget = 6250000
    maxClick = 0
    maxClickBaseBid = 0
    numImpressions = 0
    numClicked = 0
    bestC = 0
    bestCtr = 0
    bestCpm = 0
    bestCpc = 0		
    cs = []
    clicks = []
   
    testOriginal = getTestOriginalData()
    testclicks = testOriginal.iloc[:, 0].values
    testpayprice = testOriginal.iloc[:, 21].values
    
    for c in range(1, 300):
        cost = 0
        numImpressions = 0
        numClicked = 0
        bids = calculateBids(ortb_ver,preds,c)
        for i in range(len(bids)):
            testclick = testclicks[i]
            testPayPrice = testpayprice[i]
            
            if (bids[i] > testPayPrice and (cost + testPayPrice <= budget)):
                cost += testPayPrice
                numImpressions = numImpressions + 1
                numClicked = numClicked + testclick

            if (cost >= budget):
                break

        clicks.append(numClicked)
        cs.append(c)
        if(numImpressions == 0):
            continue
        ctr, cpm, cpc = calcCriteria(numClicked,numImpressions,cost)		
        
        if numClicked>maxClick:
            maxClick = numClicked
            bestC = c
            bestCtr = ctr # assigning evaluators here ties evaluators to the search which gets the most clicks,
            bestCpm = cpm # so it's not possible to see what was the search which got the highest evaluator (e.g. CTR)
            bestCpc = cpc				

    print("maxClick %f" % maxClick)
    print("bestC %f" % bestC)
    print("ctr %f" % bestCtr)
    print("cpm %f" % bestCpm)
    print("cpc %f" % bestCpc)	
    plt.plot(cs, clicks)
    plt.xlabel('c')
    plt.ylabel('Number of clicks')
    plt.show()
	
def evaluateStrategy(pred):
    budget = 6250000
    avgCTR = 0.000738
    maxClick = 0
    maxClickBaseBid = 0
    numImpressions = 0
    numClicked = 0
    cost = 0
    baseBids = []
    clicks = []
    baseBid = 78
    testOriginal = getTestOriginalData()
    testclicks = testOriginal.iloc[:, 0].values
    testpayprice = testOriginal.iloc[:, 21].values
    bestCtr = 0
    bestCpm = 0
    bestCpc = 0	
	
    for baseBid in range(10, 300):
        cost = 0.0
        numClicked = 0
        numImpressions = 0

        for i in range(len(testclicks)):
            bid = (baseBid * pred[i]) / avgCTR

            if (bid > testpayprice[i] and (cost + testpayprice[i] <= budget)):
                cost += testpayprice[i]
                numImpressions = numImpressions + 1
                numClicked = numClicked + testclicks[i]

            if (cost >= budget):
                break

        baseBids.append(baseBid)
        clicks.append(numClicked)
        if(numImpressions == 0):
            continue
        ctr, cpm, cpc = calcCriteria(numClicked,numImpressions,cost)		

        if numClicked>maxClick:
            maxClick = numClicked
            maxClickBaseBid = baseBid
            bestCtr = ctr # assigning evaluators here ties evaluators to the search which gets the most clicks,
            bestCpm = cpm # so it's not possible to see what was the search which got the highest evaluator (e.g. CTR)
            bestCpc = cpc				

    print("maxClick %f" % maxClick)
    print("maxClickBaseBid %f" % maxClickBaseBid)
    print("ctr %f" % bestCtr)
    print("cpm %f" % bestCpm)
    print("cpc %f" % bestCpc)		

    #Visualize the results
    plt.plot(baseBids, clicks)
    plt.xlabel('baseBids')
    plt.ylabel('Number of clicks')
    plt.show()
	
	
def calculateBids(ortb_ver,preds,c):
    # KPI can be CTR, CVR and other estimators, we can only use CTR as we have a lacking dataset
    l = 5.2e-7 #as per ortb paper
    bids = []
    # calculate bid using ORTB function
    for pred in preds:
        # function1: sqrt(c/l * KPI + c**2) - c # as per ortb paper
        # function2: c * (((kpi + sqrt((c*c)*(l*l) + kpi*kpi))/(c*l))**(1/3) - ((c*l)/(kpi+sqrt((c*c)*(l*l) + kpi*kpi)))**(1/3))
        bid = float(-1)
        if ortb_ver == 1:
            bid = np.sqrt(((c/l)*pred) + c**2) - c
        elif ortb_ver == 2:
            bid = c * (math.pow((pred + np.sqrt((c*c)*(l*l) + pred*pred))/(c*l),Fraction("1/3")) - math.pow((c*l)/(pred+np.sqrt((c*c)*(l*l) + pred*pred)),Fraction("1/3")))
        bids.append(bid)

    return bids	
	
def calcCriteria(numClicked,numImpressions,cost):
    ctr = (float(numClicked)/numImpressions)*100 #to turn into percentage
    cpm = (cost/numImpressions)*1000
    cpc = cost/numClicked
    return ctr, cpm, cpc