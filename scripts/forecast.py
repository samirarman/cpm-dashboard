import pandas as pd
from prophet import Prophet

sales = pd.read_csv("data/sales.csv")
sales["Data"] = pd.to_datetime(sales['Data'], format="%Y-%m-%d")
sales_per_day = sales.groupby(['Data'])['Total'].sum().reset_index()

print(sales_per_day)

dates = pd.date_range(min(sales_per_day['Data']), max(sales_per_day['Data']))
dates = pd.DataFrame({"Data":dates})
ndf = dates.merge(sales_per_day, how='left', on='Data').fillna(0).rename(columns={"Data":"ds", "Total":"y"})
print(ndf)

m = Prophet(changepoint_range=0.99, changepoint_prior_scale=0.7)
m.add_country_holidays(country_name='BR')
m.fit(ndf)

future = m.make_future_dataframe(periods=180)
forecast = m.predict(future)
forecast.to_csv("data/forecast.csv", index=False)