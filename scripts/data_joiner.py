import pandas as pd 
from glob import glob

cat = pd.read_csv("aux_data/cat.csv")
sales_reports = glob("/Users/samir/Pastas sincronizadas/Dropbox/Projeto GoCoffee/Financeiro/Relatórios do Sistema/Relatórios de Venda/Relatorio_*.xls", recursive=True)
if len(sales_reports) == 0:
    sales_reports = glob("./Relatórios de Venda/*.xls")
    
print("Found these reports:\n", sales_reports)

inventory_reports = glob("/Users/samir/Pastas sincronizadas/Dropbox/Projeto GoCoffee/Financeiro/Relatórios do Sistema/Relatórios de Estoque Detalhado/Relatorio_Estoque_*.xls")
if len(inventory_reports) == 0:
    inventory_reports = glob("./Relatórios de Estoque Detalhado/*.xls")
    
print("Found the following inventory reports:\n:", inventory_reports)

# Read exported ERP reports and output a correctly formated data
def read_sales_data(filename):
    print("Processing:", filename)
    df = pd.read_excel(filename, skiprows=3, usecols=[0,2,3,4,9,12,13])
    df.drop(df.tail(1).index, inplace = True)
    df.rename(columns={"Vl.Unit.":"Valor Unit", "Valor Total Produtos - Descontos": "Total"}, inplace=True)
    df["Data Venda"] = pd.to_datetime(df["Data Venda"],format='%d/%m/%Y %H:%M', dayfirst=True)
    df["Data"] = pd.to_datetime(df["Data Venda"].dt.date)
    df["Hora"] = df["Data Venda"].dt.time
    df["Ano"] = df['Data Venda'].dt.strftime("%Y")
    df['Mês'] = df['Data Venda'].dt.strftime("%m")
    df["Ano Mês"] = df["Data Venda"].dt.strftime('%Y-%m')
    df["Faixa Horária"] = df["Data Venda"].dt.hour
    df['Semana'] = df['Data Venda'].dt.isocalendar().week
    df["Dia da Semana"] = df["Data Venda"].dt.weekday
    df["Hora Decimal"] = df["Data Venda"].dt.hour + df["Data Venda"].dt.minute / 60
    df["Período"] = "1 - Manhã"
    df.loc[df["Data Venda"].dt.hour >= 11, ["Período"]] = "2 - Almoço"
    df.loc[df["Data Venda"].dt.hour >= 14, ["Período"]] = "3 - Tarde"
    df.loc[df["Data Venda"].dt.hour >= 18, ["Período"]] = "4 - Noite"
    return df

def read_inventory_data(filename):
    print("Processing:", filename)
    df = pd.read_excel(filename, skiprows=3)
    df.loc[df['Entrada/Saída'] == 'Saída', 'Quantidade'] *= -1
    df['Data'] = pd.to_datetime(df['Data/Hora Mov.'], dayfirst=True).dt.date
    df['Ano Mês'] = pd.to_datetime(df['Data'], dayfirst=True).dt.strftime("%Y-%m")
    df.rename(columns={'Produto   ':'Produto'}, inplace=True)
    return df

new_data = pd.concat([read_sales_data(file) for file in sales_reports]).drop_duplicates()
sales_data = new_data.merge(cat, on='Produto', how='left')
sales_data.to_csv("data/sales.csv", index=False)

inventory_data = pd.concat([read_inventory_data(file) for file in inventory_reports])
inventory_data.to_csv("data/inventory.csv", index=False)
