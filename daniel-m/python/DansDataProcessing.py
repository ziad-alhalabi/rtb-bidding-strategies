import pandas as pd
import numpy as np

TRAIN_PATH="we_data/train.csv"
VALIDATION_PATH="we_data/validation.csv"
def getData():
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(VALIDATION_PATH)
    # use: click,weekday,hour,region,slotwidth,slotheight,advertiser
    fields = ['bidid','userid','IP','domain','url','city','hour','useragent','adexchange','urlid','slotid','slotvisibility','slotformat','slotprice','creative','bidprice','payprice','keypage','usertag']

    train = train.drop(fields, axis=1)
    test = test.drop(fields, axis=1)

    X = train.iloc[:, 1:6].values # we have 7 coloumns trimmed from dataset, coloumns 1 - 6 are predictors
    Y = train.iloc[:, 0].values # coloumn 0 is predictee
    X_test = test.iloc[:, 1:6].values 
    Y_test = test.iloc[:, 0].values
    return X, Y, X_test, Y_test

#getTrainTestData()

def getTestOriginalData():
    testOriginal = pd.read_csv("we_data/validation.csv")
    return testOriginal