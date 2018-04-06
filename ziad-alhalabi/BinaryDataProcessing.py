
import pandas as pd
import numpy as np

# The classes applies some feature engineering and split the data into
# X_train, y_train, X_test, y_test. The preprocessing step includes splitting
# some columns and encoded the features into binary.

def getTrainTestData():
    # Importing the dataset
    usecols=['click', 'city', 'slotwidth', 'slotheight', 'useragent', 'slotformat', 'usertag', 'weekday', 'advertiser', 'creative', 'hour', 'slotvisibility', 'slotprice','region']
    dataset = pd.read_csv('train.csv', usecols=usecols)
    test = pd.read_csv("validation.csv", usecols=usecols)

    dataset['os'] = 'os_'+dataset['useragent'].str.split('_').str[0]
    dataset['browser'] = 'browser_'+dataset['useragent'].str.split('_').str[1]
    dataset = dataset.drop('useragent', axis=1)

    test['os'] = 'os_'+test['useragent'].str.split('_').str[0]
    test['browser'] = 'browser_'+test['useragent'].str.split('_').str[1]
    test = test.drop('useragent', axis=1)

    #Transform splitprice into buckets and binary encode them
    spsplit = []
    for index_t, row_t in dataset.iterrows():
        if row_t['slotprice'] == 0:
            spsplit.append('0')
        elif row_t['slotprice'] <= 10:
            spsplit.append('0_10')
        elif row_t['slotprice'] <= 50:
            spsplit.append('10_50')
        elif row_t['slotprice'] <= 100:
            spsplit.append('50_100')
        elif row_t['slotprice'] <= 150:
            spsplit.append('100_150')
        elif row_t['slotprice'] <= 200:
            spsplit.append('150_200')
        elif row_t['slotprice'] <= 250:
            spsplit.append('200_250')
        elif row_t['slotprice'] <= 300:
            spsplit.append('250_300')

    dataset['slotpricesplit'] = spsplit
    dummy_sp = pd.get_dummies(dataset['slotpricesplit'], prefix='slotpricesplit')
    dataset = dataset.drop('slotpricesplit', axis=1)
    dataset = dataset.drop('slotprice', axis=1)
    dataset = dataset.join(dummy_sp)
    test = test.join(dummy_sp)
    test = test.drop('slotprice', axis=1)

    #Encode hour
    browserSeries = pd.Series(dataset['hour'])
    browser_encoded_domains = pd.get_dummies(browserSeries, 'hour')
    dataset = dataset.drop('hour', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['hour'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2, 'hour')
    test = test.drop('hour', axis=1)
    test = test.join(browser_encoded_domains2)

    # Encode Region
    browserSeries = pd.Series(dataset['region'])
    browser_encoded_domains = pd.get_dummies(browserSeries, 'region')
    dataset = dataset.drop('region', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['region'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2, 'region')
    test = test.drop('region', axis=1)
    test = test.join(browser_encoded_domains2)

    #Encode weekday
    browserSeries = pd.Series(dataset['weekday'])
    browser_encoded_domains = pd.get_dummies(browserSeries, 'weekday')
    dataset = dataset.drop('weekday', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['weekday'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2, 'weekday')
    test = test.drop('weekday', axis=1)
    test = test.join(browser_encoded_domains2)

    print("weekday")
    print(list(set(browser_encoded_domains) - set(browser_encoded_domains2)))

    #Encode advertiser
    browserSeries = pd.Series(dataset['advertiser'])
    browser_encoded_domains = pd.get_dummies(browserSeries, 'advertiser')
    dataset = dataset.drop('advertiser', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['advertiser'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2, 'advertiser')
    test = test.drop('advertiser', axis=1)
    test = test.join(browser_encoded_domains2)

    print("advertiser")
    print(list(set(browser_encoded_domains) - set(browser_encoded_domains2)))


    #Encode City
    browserSeries = pd.Series(dataset['city'])
    browser_encoded_domains = pd.get_dummies(browserSeries, 'city')
    dataset = dataset.drop('city', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['city'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2, 'city')
    test = test.drop('city', axis=1)
    test = test.join(browser_encoded_domains2)

    print("city")
    print(list(set(browser_encoded_domains) - set(browser_encoded_domains2)))

    #Encode slotwidth
    browserSeries = pd.Series(dataset['slotwidth'])
    browser_encoded_domains = pd.get_dummies(browserSeries, 'slotwidth')
    dataset = dataset.drop('slotwidth', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['slotwidth'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2, 'slotwidth')
    test = test.drop('slotwidth', axis=1)
    test = test.join(browser_encoded_domains2)

    #Encode slotheight
    browserSeries = pd.Series(dataset['slotheight'])
    browser_encoded_domains = pd.get_dummies(browserSeries, 'slotheight')
    dataset = dataset.drop('slotheight', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['slotheight'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2, 'slotheight')
    test = test.drop('slotheight', axis=1)
    test = test.join(browser_encoded_domains2)



    #Encode slotvisibility
    s = pd.Series(dataset['slotvisibility'])
    encoded_domains = pd.get_dummies(s, 'slotvisibility')
    dataset = dataset.drop('slotvisibility', axis=1)
    dataset = dataset.join(encoded_domains)

    s2 = pd.Series(test['slotvisibility'])
    encoded_domains2 = pd.get_dummies(s2, 'slotvisibility')
    test = test.drop('slotvisibility', axis=1)
    test = test.join(encoded_domains2)

    #Split and encode usertag
    newDatasetColumns = dataset['usertag'].str.get_dummies(sep=',')
    dataset = dataset.drop('usertag', axis =1)
    dataset = dataset.join(newDatasetColumns)

    newTestColumns = test['usertag'].str.get_dummies(sep=',')
    test = test.drop('usertag', axis=1)
    test = test.join(newTestColumns)


    #Encode creative
    s = pd.Series(dataset['creative'])
    encoded_domains = pd.get_dummies(s, 'creative')
    dataset = dataset.drop('creative', axis=1)
    dataset = dataset.join(encoded_domains)
    dataset = dataset.drop('creative_7332', axis=1)
    dataset = dataset.drop('creative_7324', axis=1)

    s2 = pd.Series(test['creative'])
    encoded_domains2 = pd.get_dummies(s2, 'creative')
    test = test.drop('creative', axis=1)
    test = test.join(encoded_domains2)

    #Encode Slotformat
    s = pd.Series(dataset['slotformat'])
    encoded_domains = pd.get_dummies(s, 'slotformat')
    dataset = dataset.drop('slotformat', axis=1)
    dataset = dataset.join(encoded_domains)
    dataset = dataset.drop('slotformat_Na', axis=1)

    s2 = pd.Series(test['slotformat'])
    encoded_domains2 = pd.get_dummies(s2, 'slotformat')
    test = test.drop('slotformat', axis=1)
    test = test.join(encoded_domains2)
    test = test.drop('slotformat_Na', axis=1)

    #Encode Browser
    browserSeries = pd.Series(dataset['browser'])
    browser_encoded_domains = pd.get_dummies(browserSeries)
    dataset = dataset.drop('browser', axis=1)
    dataset = dataset.join(browser_encoded_domains)

    browserSeries2 = pd.Series(test['browser'])
    browser_encoded_domains2 = pd.get_dummies(browserSeries2)
    test = test.drop('browser', axis=1)
    test = test.join(browser_encoded_domains2)

    #Encode OS
    osSeries = pd.Series(dataset['os'])
    os_encoded_domains = pd.get_dummies(osSeries)
    dataset = dataset.drop('os', axis=1)
    dataset = dataset.join(os_encoded_domains)

    osSeries2 = pd.Series(test['os'])
    os_encoded_domains2 = pd.get_dummies(osSeries2)
    test = test.drop('os', axis=1)
    test = test.join(os_encoded_domains2)


    print("diff between test and dataset")
    print(list(set(test) - set(dataset)))

    X_train = dataset.iloc[:, 1:len(dataset.columns)].values
    y_train = dataset.iloc[:, 0].values

    X_test = test.iloc[:, 1:len(test.columns)].values
    y_test = test.iloc[:, 0].values

    features = list(test.drop('click', axis=1))
    print("features=======")
    print(len(features))

    features2 = list(dataset)
    print("features2=======")
    print(len(features2))

    return X_train, y_train, X_test, y_test, features, dataset, test


def getTestOriginalData():
    testOriginal = pd.read_csv("validation.csv")
    return testOriginal

def getTestBididColumn():
    usecols = ['bidid']
    dataset = pd.read_csv('test.csv', usecols=usecols)
    dataset = dataset.iloc[:, 0].values  # 0 is index of what we want to predict...
    return dataset
