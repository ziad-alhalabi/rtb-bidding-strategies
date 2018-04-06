# Importing the libraries
from encodeData import *
import pandas as pd

cols = ['click', 'weekday', 'region', 'city', 'slotwidth', 'slotheight', 'useragent', 'slotprice', 'slotformat',
               'advertiser', 'slotvisibility', 'adexchange', 'usertag']

def get_data(columns=cols):
    # Importing the dataset

    train_data = pd.read_csv('/Users/shahrozahmed/Desktop/we_data/train.csv', usecols=columns)  # training_data
    validation_data = pd.read_csv('/Users/shahrozahmed/Desktop/we_data/validation.csv', usecols=columns)

    if "click" in columns:
        columns.remove("click")
    if "payprice" in columns:
        columns.remove("payprice")

    print(columns)

    #test_data = pd.read_csv('/Users/shahrozahmed/Desktop/we_data/test.csv', usecols=columns)

    # adjust useragent
    train_data['os'] = 'os_' + train_data['useragent'].str.split('_').str[0]
    train_data['browser'] = 'browser_' + train_data['useragent'].str.split('_').str[1]
    train_data = train_data.drop('useragent', axis=1)

    validation_data['os'] = 'os_' + validation_data['useragent'].str.split('_').str[0]
    validation_data['browser'] = 'browser_' + validation_data['useragent'].str.split('_').str[1]
    validation_data = validation_data.drop('useragent', axis=1)

    #test_data['os'] = 'os_' + test_data['useragent'].str.split('_').str[0]
    #test_data['browser'] = 'browser_' + test_data['useragent'].str.split('_').str[1]
    #test_data = test_data.drop('useragent', axis=1)

    # clean data
    if "usertag" in columns:
        train_data.usertag = clean_data(train_data.usertag)
        validation_data.usertag = clean_data(validation_data.usertag)

    # Encode variables
    train_data = encode_all(train_data, columns)
    validation_data = encode_all(validation_data, columns)

    val_features = list(validation_data)
    train_features = list(train_data)
    train_data = train_data[val_features]

    #test_data = encode_all(test_data, columns)

    '''
    val_features = list(validation_data)
    train_features = list(train_data)

    if train_features != val_features:
        keep = list()
        remove = list()

        for f in val_features:
            if f in train_features:
                keep.append(f)
            else:
                remove.append(f)

        

        train_data = train_data[keep]
        validation_data = validation_data[keep]
        '''



    #print(train_data)
    # determine data rows
    X_train = train_data.iloc[:, 1:len(train_data.columns)].values  # drop clicks
    y_train = train_data.iloc[:, 0].values  # predict clicks

    X_valid = validation_data.iloc[:, 1:len(train_data.columns)].values  # drop clicks
    y_valid = validation_data.iloc[:, 0].values  # predict clicks

    #X_test = test_data.iloc[:, 0:len(train_data.columns)].values  # only need X

    # features being used in validation data
    features = list(validation_data.drop('click', axis=1))
    print("features count=======")
    print(len(features))

    features2 = list(train_data)
    print("features count=======")
    print(len(features2))

    return X_train, y_train, X_valid, y_valid, features, train_data, validation_data


