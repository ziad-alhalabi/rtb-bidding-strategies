
import pandas as pd

# This class parses the datasets and applies encoding on the features
# and returns the X and y for training and testing


def getTrainTestData():

    usecols = ['click', 'city', 'region', 'slotwidth', 'slotheight', 'useragent', 'slotprice', 'usertag', 'weekday', 'advertiser', 'slotvisibility', 'domain']
    dataset = pd.read_csv('train.csv', usecols=usecols)
    test = pd.read_csv("validation.csv", usecols=usecols)

    # Split useragent into OS and browser
    dataset['os'] = 'os_'+dataset['useragent'].str.split('_').str[0]
    dataset['browser'] = 'browser_'+dataset['useragent'].str.split('_').str[1]
    dataset = dataset.drop('useragent', axis=1)

    test['os'] = 'os_'+test['useragent'].str.split('_').str[0]
    test['browser'] = 'browser_'+test['useragent'].str.split('_').str[1]
    test = test.drop('useragent', axis=1)


    # Encode slotvisibility
    s = pd.Series(dataset['slotvisibility'])
    encoded_domains = pd.get_dummies(s, 'slotvisibility')
    dataset = dataset.drop('slotvisibility', axis=1)
    dataset = dataset.join(encoded_domains)

    s2 = pd.Series(test['slotvisibility'])
    encoded_domains2 = pd.get_dummies(s2, 'slotvisibility')
    test = test.drop('slotvisibility', axis=1)
    test = test.join(encoded_domains2)

    # Split and encode usertag
    newDatasetColumns = dataset['usertag'].str.get_dummies(sep=',')
    dataset = dataset.drop('usertag', axis =1)
    dataset = dataset.join(newDatasetColumns)

    newTestColumns = test['usertag'].str.get_dummies(sep=',')
    test = test.drop('usertag', axis=1)
    test = test.join(newTestColumns)

    # Encode Browser
    browserSeries = pd.Series(dataset['browser'])
    browser_encoded_domains = pd.get_dummies(browserSeries)
    dataset = dataset.drop('browser', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['browser'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2)
    test = test.drop('browser', axis=1)
    test = test.join(browser_encoded_domains2)

    # Encode OS
    osSeries = pd.Series(dataset['os'])
    os_encoded_domains = pd.get_dummies(osSeries)
    dataset = dataset.drop('os', axis=1)
    dataset = dataset.join(os_encoded_domains)

    osSeries2 = pd.Series(test['os'])
    os_encoded_domains2 = pd.get_dummies(osSeries2)
    test = test.drop('os', axis=1)
    test = test.join(os_encoded_domains2)

    X_train = dataset.iloc[:, 1:len(dataset.columns)].values
    y_train = dataset.iloc[:, 0].values

    X_test = test.iloc[:, 1:len(test.columns)].values
    y_test = test.iloc[:, 0].values

    features = list(test.drop('click', axis=1))

    return X_train, y_train, X_test, y_test, features, dataset, test


def getTestOriginalData():
    testOriginal = pd.read_csv("validation.csv")
    return testOriginal

def getTestBididColumn():
    usecols = ['bidid']
    dataset = pd.read_csv('test.csv', usecols=usecols)
    dataset = dataset.iloc[:, 0].values
    return dataset
