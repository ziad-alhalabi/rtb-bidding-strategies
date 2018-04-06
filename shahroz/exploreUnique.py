import pandas as pd
import numpy as np

train_data = pd.read_csv('/Users/shahrozahmed/Desktop/we_data/train.csv')  # training_data

data_frame = pd.DataFrame(train_data)

print("Weekday:", len(data_frame.weekday.unique()))
print("Hour:", len(data_frame.hour.unique()))
print("BidID:", len(data_frame.bidid.unique()))
print("userId:", len(data_frame.userid.unique()))
print("Useragent:", len(data_frame.useragent.unique()))
print("IP:", len(data_frame.IP.unique()))
print("Region:", len(data_frame.region.unique()))
print("City:", len(data_frame.city.unique()))
print("Adexchange:", len(data_frame.adexchange.unique()))
print("Domain:", len(data_frame.domain.unique()))
print("URL:", len(data_frame.url.unique()))
print("URLId:", len(data_frame.urlid.unique()))
print("SlotId:", len(data_frame.slotid.unique()))
print("SlotWidth:", len(data_frame.slotwidth.unique()))
print("SlotHeight:", len(data_frame.slotheight.unique()))
print("SlotVisibility:", len(data_frame.slotvisibility.unique()))
print("SlotFormat:", len(data_frame.slotformat.unique()))
print("SlotPrice:", len(data_frame.slotprice.unique()))
print("Creative:", len(data_frame.creative.unique()))
print("Payprice:", len(data_frame.payprice.unique()))
print("Keypage:", len(data_frame.keypage.unique()))
print("Advertiser:", len(data_frame.advertiser.unique()))

ut = data_frame.usertag
unique = []

for i in ut:
    if isinstance(i, str):
        split = i.split(',')
        for u in split:
            if u not in unique:
                unique.append(u)
print("Usertag:", len(unique))