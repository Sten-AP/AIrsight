import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datasets")
df = pd.read_csv(os.path.join(DATASET_DIR, "merged_data.csv"))


numeric_df = df.select_dtypes(include=[np.number])

correlation = numeric_df.corr()
correlation = correlation.dropna(how='all')
correlation = correlation.dropna(axis=1, how='all')
print(correlation)
plt.figure(figsize=(10,8))
sns.heatmap(correlation, annot=True, cmap='coolwarm',fmt=".2f")
plt.show()