import pandas as pd

df = pd.read_csv('model\calls\datasets\wekeo_data.csv')
df.drop("local_date", axis=1, inplace=True)

correlation = df.corr()

print(correlation)

