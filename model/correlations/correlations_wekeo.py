import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

datasets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".." , "calls", "multiple_sensors", "datasets")
df = pd.read_csv(os.path.join(datasets_dir, "wekeo_data.csv"))
df.drop("local_date", axis=1, inplace=True)
df.drop("Unnamed: 0_x", axis=1, inplace=True)
df.drop("Unnamed: 0_y", axis=1, inplace=True)

correlation = df.corr()
print(correlation)
plt.figure(figsize=(10,8))
sns.heatmap(correlation, annot=True, cmap='coolwarm',fmt=".2f")
plt.show()