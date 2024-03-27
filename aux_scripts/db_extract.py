import pandas as pd
import sqlite3

con = sqlite3.connect("/Users/Samir/Documents/py-proj/inventory-control/purchases.db")
cur = con.cursor()

ldm = pd.read_sql_query("SELECT * FROM boms_view", con)
ldm.to_csv("ldm.csv", index=False)

purchases = pd.read_sql_query("SELECT * FROM excel_exporter", con, parse_dates=True)
purchases = purchases.iloc[:,[0,2,11,12,13,14,15,16,17,19,]].set_axis(['date', 'material', 'price', 'disc', 'freight', 'icms_st', 'difal', 'ipi', 'total', 'qty'], axis=1)
purchases['unit_price'] = purchases['price']/purchases['qty']
purchases['unit_cost'] = purchases['total']/purchases['qty']
purchases['surcharge'] = purchases['total']/purchases['price'] - 1
purchases['date'] = pd.to_datetime(purchases['date'])
purchases['year_month'] = purchases['date'].dt.strftime('%Y-%m')
purchases.to_csv("purchases.csv", index=False)

