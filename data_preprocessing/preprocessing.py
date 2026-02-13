import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

full_df = pd.read_csv('data/CICIDS2017_Combined.csv')

full_df["Traffic_Type"] = full_df["Label"].apply(
    lambda x: "BENIGN" if x == "BENIGN" else "ATTACK"
)

# print(full_df["Label"].value_counts())

# full_df.isnull().sum()
# full_df.describe()
# full_df.info()
# full_df.columns
# full_df.shape
# full_df.duplicated().sum()

print(full_df.head())