import pandas as pd

df = pd.read_csv("../data/inventory.csv")
df['Data'] = pd.to_datetime(df['Data/Hora Mov.'], dayfirst=True)
df['Data'] = pd.to_datetime(df['Data'].dt.date)
df['Ano'] = df['Data'].dt.year
df['Semana'] = df['Data'].dt.isocalendar().week
print(df)

consumption = df[(df['Entrada/Saída'] == 'Saída') & (df['Tipo'] == 'Saída')]
consumption = consumption.groupby(['Ano', 'Data', 'Produto'])['Quantidade'].sum().reset_index()
print(consumption)

demand = daily_consumption.groupby('Produto')['Quantidade'].agg(lambda x : 0.7 * x.tail(30).mean() + 0.3 * x.tail(120).mean()).reset_index()
demand.rename(columns={'Quantidade':'Demanda'}, inplace=True)
print(demand)

levels = df.groupby(['Produto', 'Tipo', 'Entrada/Saída'])['Quantidade'].sum().reset_index().groupby('Produto')['Quantidade'].sum().reset_index().rename(columns={'Quantidade':'Saldo'})
print(levels)

demand = demand.merge(levels, on='Produto', how='right')
demand["Dias para o fim"] = round(-demand["Saldo"]/demand["Demanda"], 0)
demand.loc[demand["Saldo"] <= 0, "Dias para o fim"] = 0
print(demand)

demand.to_csv("../data/inventory_demand.csv", index=False)