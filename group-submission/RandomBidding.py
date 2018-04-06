import matplotlib.pyplot as plt
from random import *
import pandas as pd
# File Paths
TRAIN_PATH = "we_data/train.csv"
VALIDATION_PATH = "we_data/validation.csv"

def main():
    budget = 6250000
    maxClick = 0
    bestLowerBound = 1
    bestUpperBound = 0
    numImpressions = 0
    numClicked = 0
    cost = 0
    upperBounds = []
    lowerBounds = []
    clicks = []
    bestCtr = 0
    bestCpm = 0
    bestCpc = 0	
    testClicks, testPayPrices = getTestData()
    """
	
    Find the most optimal upper-bound bid.
	
    """
    for search in range(bestLowerBound, 1500):
        cost = 0.0
        numClicked = 0
        numImpressions = 0
        lowerBound = 1
        upperBound = search
        for i in range(len(testClicks)):
            testclick = testClicks[i]
            
            testPayPrice = testPayPrices[i]

            bid = randint(lowerBound,upperBound) #upperBound is the variable one here

            if (bid > testPayPrice and (cost + testPayPrice <= budget)):
                cost += testPayPrice
                numImpressions = numImpressions + 1
                numClicked = numClicked + testclick

            if (cost >= budget):
                break

        ctr, cpm, cpc = calcCriteria(numClicked,numImpressions,cost)

        upperBounds.append(upperBound)
        clicks.append(numClicked)

        if numClicked>maxClick:
            maxClick = numClicked
            bestUpperBound = upperBound
            bestCtr = ctr # assigning evaluators here ties evaluators to the search which gets the most clicks,
            bestCpm = cpm # so it's not possible to see what was the search which got the highest evaluator (e.g. CTR)
            bestCpc = cpc			

    
    #Visualize the results
    plt.plot(upperBounds, clicks)
    plt.xlabel('Upper bound')
    plt.ylabel('Number of clicks')
    plt.show()	
    print("Best upper bound %f" % bestUpperBound)
    upperBound = bestUpperBound + 1
    clicks = []
	
    """
	
    Find the most optimal lower-bound bid by reducing the gap between the lower and upper bounds.
	
    """	
    for search in range(1,upperBound):
        cost = 0.0
        numClicked = 0
        numImpressions = 0
        lowerBound = search
        for i in range(len(testClicks)):
            testclick = testClicks[i]
            
            testPayPrice = testPayPrices[i]

            bid = randint(lowerBound,bestUpperBound) # the variable value here is lowerBound

            if (bid > testPayPrice and (cost + testPayPrice <= budget)):
                cost += testPayPrice
                numImpressions = numImpressions + 1
                numClicked = numClicked + testclick

            if (cost >= budget):
                break


        ctr, cpm, cpc = calcCriteria(numClicked,numImpressions,cost)

        lowerBounds.append(lowerBound)
        clicks.append(numClicked)

        if numClicked>maxClick:
            maxClick = numClicked
            bestLowerBound = lowerBound
            bestCtr = ctr # assigning evaluators here ties evaluators to the search which gets the most clicks,
            bestCpm = cpm # so it's not possible to see what was the search which got the highest evaluator (e.g. CTR)
            bestCpc = cpc			

    print("Most clicks achieved %f" % maxClick)
    print("Lower/Upper bounds for most clicks achieved:")
    print("Best lower bound %f" % bestLowerBound)
    print("Best upper bound %f" % bestUpperBound)
    print("ctr %f" % bestCtr)
    print("cpm %f" % bestCpm)
    print("cpc %f" % bestCpc)	

    #Visualize the results
    plt.plot(lowerBounds, clicks)
    plt.xlabel('Lower bounds')
    plt.ylabel('Number of clicks')
    plt.show()
	
    """

    Now verify that the found bounds indeed reliably produce optimal number of clicks
    
    """
    print("Verifying...")
    numImpressions = 0
    numClicked = 0
    cost = 0
    upperBounds = []
    lowerBounds = []
    clicks = []
    bestCtr = 0
    bestCpm = 0
    bestCpc = 0		
    lower = bestLowerBound
    upper = bestUpperBound
    maxClick = 0
    
    for l in range(lower,upper):
        cost = 0.0
        numClicked = 0
        numImpressions = 0
        for i in range(len(testClicks)):
            testclick = testClicks[i]
            
            testPayPrice = testPayPrices[i]

            bid = randint(l,upper)

            if (bid > testPayPrice and (cost + testPayPrice <= budget)):
                cost += testPayPrice
                numImpressions = numImpressions + 1
                numClicked = numClicked + testclick

            if (cost >= budget):
                break


        ctr, cpm, cpc = calcCriteria(numClicked,numImpressions,cost)
        
        if numClicked>maxClick:
            maxClick = numClicked
            bestCtr = ctr # assigning evaluators here ties evaluators to the search which gets the most clicks,
            bestCpm = cpm # so it's not possible to see what was the search which got the highest evaluator (e.g. CTR)
            bestCpc = cpc		
			
    print("Most clicks achieved %f" % maxClick)
    print("Lower/Upper bounds for most clicks achieved:")
    print("Best lower bound %f" % bestLowerBound)
    print("Best upper bound %f" % bestUpperBound)
    print("ctr %f" % bestCtr)
    print("cpm %f" % bestCpm)
    print("cpc %f" % bestCpc)
	
def calcCriteria(numClicked,numImpressions,cost):
    ctr = (float(numClicked)/numImpressions)*100 #to turn into percentage
    cpm = (cost/numImpressions)*1000
    cpc = cost/numClicked
    return ctr, cpm, cpc
	
def getTestData():
    testOriginal = pd.read_csv(VALIDATION_PATH)
    testClicks = testOriginal.iloc[:, 0].values
    testPayPrices = testOriginal.iloc[:, 21].values
    return testClicks, testPayPrices
	
if __name__ == "__main__":
    main()