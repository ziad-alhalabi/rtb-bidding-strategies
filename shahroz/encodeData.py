import pandas as pd


#Encode variables
def encode_var(dataset, variable):
    series = pd.Series(dataset[variable])
    encoded_domains = pd.get_dummies(series)
    dataset = dataset.drop(variable, axis=1)
    dataset = dataset.join(encoded_domains)
    return dataset


def encode_hard(dataset, variable):
    series = pd.Series(dataset[variable])
    dataset = pd.concat([dataset, pd.get_dummies(series, prefix=variable)], axis=1)
    dataset = dataset.drop(variable, axis=1)
    return dataset


def encode_region(dataset):
    series = pd.Series(dataset['region'])
    dataset = pd.concat([dataset, pd.get_dummies(series, prefix='region')], axis=1)
    dataset = dataset.drop('region', axis=1)
    return dataset


def encode_adexchange(dataset):
    return encode_var(dataset, 'adexchange')


def encode_slotwidth(dataset):
    return encode_hard(dataset, 'slotwidth')


def encode_slotheight(dataset):
    return encode_var(dataset, 'slotheight')


def encode_advertiser(dataset):
    return encode_var(dataset, 'advertiser')


def encode_slotvisibility(dataset):
    s = pd.Series(dataset['slotvisibility'])
    encoded_domains = pd.get_dummies(s, 'slotvisibility')
    dataset = dataset.drop('slotvisibility', axis=1)
    dataset = dataset.join(encoded_domains)
    return dataset

def encode_slotformat(dataset):
    return encode_var(dataset, 'slotformat')


def encode_browser(dataset):
    return encode_var(dataset, 'browser')


def encode_os(dataset):
    return encode_var(dataset, 'os')


def encode_slotprice(dataset):
    return encode_hard(dataset, 'slotprice')


def encode_payprice(dataset):
    return encode_hard(dataset, 'payprice')


def encode_hours(dataset):
    return encode_hard(dataset, 'hour')


def encode_weekday(dataset):
    series = pd.Series(dataset["weekday"])
    dataset = pd.concat([dataset, pd.get_dummies(series, prefix='day')], axis=1)
    dataset = dataset.drop('weekday', axis=1)
    return dataset


def encode_usertags(dataframe):
    usertags = list(dataframe.usertag)
    unique_tag = set()
    list_ut = []
    for user in usertags:
        # print("this is user: ", user)
        if isinstance(user, str):
            u = user.split(',')
            list_ut.append(u)
            for us in u:
                unique_tag.add(us)
    users = pd.DataFrame()
    for user in unique_tag:
        users["user_" + user] = 0
    dataframe = pd.concat([dataframe, users], axis=1)
    for user in unique_tag:
        datas = []
        for users in list_ut:
            if user in users:
                datas.append(1)
            else:
                datas.append(0)

                # print(user, isinstance(user, str))
        dataframe["user_" + user] = pd.Series(datas)
    dataframe = dataframe.drop('usertag', axis=1)
    return dataframe


def optimise_domain(data, domain_keep_prob=0.04):
    unique_domain = data['domain'].value_counts()
    threshold = int(domain_keep_prob * len(unique_domain))
    domain_threshold = unique_domain[threshold]
    data['domain'].where(data['domain'].map(unique_domain) > domain_threshold, "unpopularFeatures", inplace=True)
    return encode_var(data, 'domain')


def encode_all(data, cols):
    if "domain" in cols:
        data = optimise_domain(data)
    if "adexchange" in cols:
        data = encode_adexchange(data)
    if "advertiser" in cols:
        data = encode_advertiser(data)
    if "hour" in cols:
        data = encode_hours(data)
    if "useragent" in cols:
        data = encode_os(data)
    if "useragent" in cols:
        data = encode_browser(data)
    if "region" in cols:
        data = encode_region(data)
    if "slotformat" in cols:
        data = encode_slotformat(data)
    if "slotvisibility" in cols:
        data = encode_slotvisibility(data)
    if "usertag" in cols:
        data = encode_usertags(data)
    if "weekday" in cols:
        data = encode_weekday(data)

    #data = encode_slotheight(data)
    #data = encode_slotprice(data)
    #data = encode_slotvisibility(data)
    #data = encode_slotwidth(data)
    #data = encode_payprice(data)
    #data = encode_usertags(data)
    return data


def clean_data(dataset):
    dataset = dataset.apply(pd.to_numeric, errors='coerce')
    dataset = dataset.replace('NaN', 0)
    return dataset


def remove_features(features_list, regressor):
    features = pd.DataFrame(features_list, regressor.feature_importances_)
    features = features.sort_index(ascending=False)
    features.reset_index(level=0, inplace=True)
    features = features.rename(columns={'index': 'values', 0: 'feature'})
    features_keep = features[features['values'] > 0.0001]
    features_removed = features[features['values'] <= 0.0001]
    features_selected = list(features_keep['feature'].values)

    print("features selected")
    print(features_keep)
    print("features removed")
    print(features_removed)

    return features_selected

