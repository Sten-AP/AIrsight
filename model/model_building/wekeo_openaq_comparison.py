import pandas as pd
from sklearn.metrics import mean_absolute_error
import os

datasets_dir = os.path.dirname("model\calls\datasets")

merged_data = pd.read_csv("model/calls/datasets/merged_data.csv")

if 'pm25_x' in merged_data.columns and 'pm25_y' in merged_data.columns:
    baseline_mae = mean_absolute_error(merged_data['pm25_x'], merged_data['pm25_y'])
    print(f'Baseline Mean Absolute Error between pm25_x(wekeo) and pm25_y(openAQ): {baseline_mae}')
if 'pm10_x' in merged_data.columns and 'pm10_y' in merged_data.columns:
    baseline_mae = mean_absolute_error(merged_data['pm10_x'], merged_data['pm10_y'])
    print(f'Baseline Mean Absolute Error between pm10_x(wekeo) and pm25_y(openAQ): {baseline_mae}')
if 'no2_x' in merged_data.columns and 'no2_y' in merged_data.columns:
    baseline_mae = mean_absolute_error(merged_data['no2_x'], merged_data['no2_y'])
    print(f'Baseline Mean Absolute Error between no2_x and _y: {baseline_mae}')