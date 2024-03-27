import pandas as pd

pd.read_excel("prod_data.xlsx").to_csv("aux_data/prod_data.csv", index=False)