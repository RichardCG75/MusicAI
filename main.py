import pandas as pd

song1 = [[1,4], [2,4], [3,4]]
song2 = [[2,4], [3,4], [4,4]]

dataFrame1 = pd.DataFrame({'Song1': song1})
dataFrame2 = pd.DataFrame({'Song2': song2})

finalDataFrame = pd.concat([dataFrame1, dataFrame2], axis=1)

print('=== Data Frame 1 ===')
print(finalDataFrame)
finalDataFrame.to_csv('data.csv', index=False)

print('=== One Hot Enc ===')
# oneHotEnc = pd.get_dummies(finalDataFrame)

df = pd.DataFrame({'Color': ['Red', 'Green', 'Blue', 'Red']})

# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['Color'])
print(df_encoded)
# print()