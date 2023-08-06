import simple_data_feeder as feeder

train, test = feeder.getData('data/bot_dataset1.csv', 0.7)

print(train)
print(test)
