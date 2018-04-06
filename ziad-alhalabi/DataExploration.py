import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# This file contains functions that outputs interesting relations between
# the dataset features. It outputs tables and plots.

trainDataset = pd.read_csv('train.csv')
trainDataset['os'] = '' + trainDataset['useragent'].str.split('_').str[0]
trainDataset['browser'] = '' + trainDataset['useragent'].str.split('_').str[1]


# Plots Pearson Correlation between certain features
def plot_heat_map():
    colormap = plt.cm.RdBu
    usecols = ['click','slotwidth', 'slotheight', 'slotprice',
                'bidprice', 'payprice', 'hour', 'weekday']
    dataset = trainDataset[usecols]
    plt.figure(figsize=(10, 10))
    plt.title('Pearson Correlation of Features', y=1.05, size=15)
    sns.heatmap(dataset.astype(float).corr(), linewidths=0.1, vmax=1.0,
                square=True, cmap=colormap, linecolor='white', annot=True)

def describe_prices():
    # outputing table
    print(trainDataset['bidprice'].describe())
    print(trainDataset['payprice'].describe())
    print(trainDataset['slotprice'].describe())


def ad_data_statistics(data):
    advertisers = list(Counter(data.advertiser))
    df = pd.DataFrame()
    df['Advertiser'] = advertisers
    df['Bids'] = [len(data[data.advertiser == i].bidprice) for i in advertisers]

    # An Impression is when the bidprice > payprice
    df['Impressions'] = [sum(((data[data.advertiser == i]).bidprice > (data[data.advertiser == i]).payprice)) for i in advertisers]

    df['Clicks'] = [sum((data[data.advertiser == i]).click) for i in advertisers]

    # The sum of the pay price when a bid was won
    df['Cost'] = [sum(data[data.advertiser == i][data.bidprice > data.payprice].payprice / 1000) for i in advertisers]

    df['CTR'] = [sum((data[data.advertiser == i]).click / len(data[data.advertiser == i])) for i in advertisers]

    # CPM: cost per thousand impressions
    df['CPM'] = df['Cost'] / (df['Impressions'] / 1000)

    df['eCPC'] = df['Cost'] / df['Clicks']
    print(df)


# Plots the CTR versus Weekday for the given advertisers
def plot_advertisers_ctr_weekday(advertisers):
    adv="advertiser"
    plt.figure(figsize=(10,6))
    for advertiser in advertisers:
        mean=trainDataset.groupby(["weekday",adv]).mean()
        y=mean.unstack(adv)["click"][advertiser]
        x = y.index
        plt.errorbar(x=x,y=y)

    plt.xlabel("Weekday")
    plt.ylabel("CTR")
    plt.legend(advertisers, loc=2)
    plt.show()


# Plots the CTR versus Hour for the given advertisers
def plot_advertisers_ctr_hour(advertisers):
    adv="advertiser"
    plt.figure(figsize=(10,6))
    for advertiser in advertisers:
        mean=trainDataset.groupby(["hour",adv]).mean()
        y=mean.unstack(adv)["click"][advertiser]
        x = y.index
        plt.errorbar(x=x,y=y)

    plt.xlabel("Hour")
    plt.ylabel("CTR")
    plt.legend(advertisers, loc=2)
    plt.show()


# Plots the CTR versus Region for the given advertisers
def plot_advertisers_ctr_region(advertisers):
    adv="advertiser"
    plt.figure(figsize=(10,6))
    for advertiser in advertisers:
        mean=trainDataset.groupby(["region",adv]).mean()
        y=mean.unstack(adv)["click"][advertiser]
        x = y.index
        plt.errorbar(x=x,y=y)

    plt.xlabel("Region")
    plt.ylabel("CTR")
    plt.legend(advertisers, loc=2)
    plt.show()


# Plots the mean Slotprice and Bidprice versus Day for all advertisers
def plot_slotprice_bidprice_day():
    x_indexes = trainDataset.iloc[:, 1].values
    y_indexes = trainDataset.iloc[:, 18].values

    y_indexes2 = trainDataset.iloc[:, 20].values
    y_indexes3 = trainDataset.iloc[:, 21].values

    df = pd.DataFrame(y_indexes, columns=["values"], index=x_indexes)
    result = df.groupby(df.index).mean()
    print(result)

    df2 = pd.DataFrame(y_indexes2, columns=["values"], index=x_indexes)
    result2 = df2.groupby(df2.index).mean()
    print(result2)

    df3 = pd.DataFrame(y_indexes3, columns=["values"], index=x_indexes)
    result3 = df3.groupby(df3.index).mean()
    print(result3)

    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(111)
    ax1.plot(result, 'tab:blue')
    ax1.set_ylabel('Slot Price', color='tab:blue')
    ax1.set_xlabel('Weekday')
    for tl in ax1.get_yticklabels():
        tl.set_color('tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(result2, 'tab:orange')
    ax2.set_ylabel('Bid Price', color='tab:orange')
    for tl in ax2.get_yticklabels():
        tl.set_color('tab:orange')

    plt.show()


# Plots the mean Bidprice and Payprice versus Day for all advertisers
def plot_bidprice_payprice_day():
    x_indexes = trainDataset.iloc[:, 1].values

    y_indexes2 = trainDataset.iloc[:, 20].values
    y_indexes3 = trainDataset.iloc[:, 21].values

    df = pd.DataFrame(y_indexes2, columns=["values"], index=x_indexes)
    result = df.groupby(df.index).mean()
    print(result)

    df3 = pd.DataFrame(y_indexes3, columns=["values"], index=x_indexes)
    result3 = df3.groupby(df3.index).mean()
    print(result3)

    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(111)
    ax1.plot(result)
    ax1.set_ylabel('Bid Price', color='tab:blue')
    ax1.set_xlabel('Weekday')
    for tl in ax1.get_yticklabels():
        tl.set_color('tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(result3, 'tab:orange')
    ax2.set_ylabel('Pay Price', color='tab:orange')
    for tl in ax2.get_yticklabels():
        tl.set_color('tab:orange')

    plt.show()


# Plots the mean Slotprice and Bidprice versus Hour for all advertisers
def plot_slotprice_bidprice_hour():
    x_indexes = trainDataset.iloc[:, 2].values
    y_indexes = trainDataset.iloc[:, 18].values

    y_indexes2 = trainDataset.iloc[:, 20].values

    df = pd.DataFrame(y_indexes, columns=["values"], index=x_indexes)
    result = df.groupby(df.index).mean()
    print(result)

    df2 = pd.DataFrame(y_indexes2, columns=["values"], index=x_indexes)
    result2 = df2.groupby(df2.index).mean()
    print(result2)

    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(111)
    ax1.plot(result)
    ax1.set_ylabel('Slot Price', color='tab:blue')
    ax1.set_xlabel('Hour')
    for tl in ax1.get_yticklabels():
        tl.set_color('tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(result2, 'tab:orange')
    ax2.set_ylabel('Bid Price', color='tab:orange')
    for tl in ax2.get_yticklabels():
        tl.set_color('tab:orange')

    plt.show()

# Plots the mean Bidprice and Payprice versus Day for all advertisers
def plot_bidprice_payprice_region():
    x_indexes = trainDataset.iloc[:, 7].values

    y_indexes2 = trainDataset.iloc[:, 20].values
    y_indexes3 = trainDataset.iloc[:, 21].values

    df = pd.DataFrame(y_indexes2, columns=["values"], index=x_indexes)
    result = df.groupby(df.index).mean()
    print(result)

    df3 = pd.DataFrame(y_indexes3, columns=["values"], index=x_indexes)
    result3 = df3.groupby(df3.index).mean()
    print(result3)

    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(111)
    ax1.plot(result)
    ax1.set_ylabel('Bid Price', color='tab:blue')
    ax1.set_xlabel('Region')
    for tl in ax1.get_yticklabels():
        tl.set_color('tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(result3, 'tab:orange')
    ax2.set_ylabel('Pay Price', color='tab:orange')
    for tl in ax2.get_yticklabels():
        tl.set_color('tab:orange')

    plt.show()


# Plots the mean Slotprice and Bidprice versus Region for all advertisers
def plot_slotprice_bidprice_region():
    x_indexes = trainDataset.iloc[:, 7].values
    y_indexes = trainDataset.iloc[:, 18].values

    y_indexes2 = trainDataset.iloc[:, 20].values

    df = pd.DataFrame(y_indexes, columns=["values"], index=x_indexes)
    result = df.groupby(df.index).mean()
    print(result)

    df2 = pd.DataFrame(y_indexes2, columns=["values"], index=x_indexes)
    result2 = df2.groupby(df2.index).mean()
    print(result2)

    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(111)
    ax1.plot(result)
    ax1.set_ylabel('Slot Price', color='tab:blue')
    ax1.set_xlabel('Region')
    for tl in ax1.get_yticklabels():
        tl.set_color('tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(result2, 'tab:orange')
    ax2.set_ylabel('Bid Price', color='tab:orange')
    for tl in ax2.get_yticklabels():
        tl.set_color('tab:orange')

    plt.show()


# Plots the mean Bidprice and Payprice versus Hour for all advertisers
def plot_bidprice_payprice_hour():
    x_indexes = trainDataset.iloc[:, 2].values

    y_indexes2 = trainDataset.iloc[:, 20].values
    y_indexes3 = trainDataset.iloc[:, 21].values

    df = pd.DataFrame(y_indexes2, columns=["values"], index=x_indexes)
    result = df.groupby(df.index).mean()
    print(result)

    df3 = pd.DataFrame(y_indexes3, columns=["values"], index=x_indexes)
    result3 = df3.groupby(df3.index).mean()
    print(result3)

    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(111)
    ax1.plot(result)
    ax1.set_ylabel('Bid Price', color='tab:blue')
    ax1.set_xlabel('Hour')
    for tl in ax1.get_yticklabels():
        tl.set_color('tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(result3, 'tab:orange')
    ax2.set_ylabel('Pay Price', color='tab:orange')
    for tl in ax2.get_yticklabels():
        tl.set_color('tab:orange')

    plt.show()


# Plots the mean CTR versus Browser for all advertisers
def plot_advertisers_ctr_browser():
    advertisers = list(Counter(trainDataset.advertiser))
    adv="advertiser"
    plt.figure(figsize=(10,6))
    for advertiser in advertisers:
        mean=trainDataset.groupby(["browser",adv]).mean()
        y=mean.unstack(adv)["click"][advertiser]
        x = y.index
        plt.errorbar(x=x,y=y, marker="o",linestyle="")

    plt.xlabel("Browser")
    plt.ylabel("CTR")
    plt.legend(advertisers, loc=1)
    plt.show()


# Plots the mean CTR versus OS for all advertisers
def plot_advertisers_ctr_os():
    advertisers = list(Counter(trainDataset.advertiser))
    adv="advertiser"
    plt.figure(figsize=(10,6))
    for advertiser in advertisers:
        mean=trainDataset.groupby(["os",adv]).mean()
        y=mean.unstack(adv)["click"][advertiser]
        x = y.index
        plt.errorbar(x=x, y=y, marker="o", linestyle="")

    plt.xlabel("OS")
    plt.ylabel("CTR")
    plt.legend(advertisers, loc=1)
    plt.show()


# Example Plotting
list_advert=[1458,3358]
#list_advert = list(Counter(trainDataset.advertiser)) #all adver
plot_advertisers_ctr_os()





