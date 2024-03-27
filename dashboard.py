import streamlit as st
import pandas as pd
from glob import glob
import datetime as datetime
import numpy as np
import sqlite3

##########
# SETUP
##########
# con = sqlite3.connect("/Users/Samir/Documents/py-proj/inventory-control/purchases.db")
# cur = con.cursor()

st.title('Cafeteria Patteo Mogilar')
kpi_tab, cogs_tab, material_tab, datasets_tab, inventory_tab = st.tabs(["KPI", "Cost Data", "Material Data", "Datasets", "Estoque"])

##########
# DATA PREPARATION
##########
cat = pd.read_csv("aux_data/cat.csv")
# reports = glob("/Users/samir/Pastas sincronizadas/Dropbox/Projeto GoCoffee/Financeiro/Relatórios do Sistema/Relatórios de Venda/Relatorio_*.xls", recursive=True)
# reports = glob("/Users/samir/Library/CloudStorage/Dropbox/Projeto GoCoffee/Financeiro/Relatórios do Sistema/Relatórios de Venda/Relatorio_*.xls", recursive=True)
# delivery_reports = glob("/Users/samir/Pastas sincronizadas/Dropbox/Projeto GoCoffee/Financeiro/Relatórios do Sistema/Relatórios de Delivery/Relatorio_*.xls", recursive=True)
# delivery_reports = glob("/Users/samir/Library/CloudStorage/DDropbox/Projeto GoCoffee/Financeiro/Relatórios do Sistema/Relatórios de Delivery/Relatorio_*.xls", recursive=True)

# @st.cache_data
# def read_data(filename):
#     print("Processing:", filename)
#     df = pd.read_excel(filename, skiprows=3, usecols=[0,2,3,4,9,12,13])
#     df.drop(df.tail(1).index, inplace = True)
#     df.rename(columns={"Vl.Unit.":"Valor Unit", "Valor Total Produtos - Descontos": "Total"}, inplace=True)
#     df["Data Venda"] = pd.to_datetime(df["Data Venda"],format='%d/%m/%Y %H:%M', dayfirst=True)
#     df["Data"] = pd.to_datetime(df["Data Venda"].dt.date)
#     df["Hora"] = df["Data Venda"].dt.time
#     df["Ano"] = df['Data Venda'].dt.strftime("%Y")
#     df['Mês'] = df['Data Venda'].dt.strftime("%m")
#     df["Ano Mês"] = df["Data Venda"].dt.strftime('%Y-%m')
#     df["Faixa Horária"] = df["Data Venda"].dt.hour
#     df["Dia da Semana"] = df["Data Venda"].dt.weekday
#     df["Hora Decimal"] = df["Data Venda"].dt.hour + df["Data Venda"].dt.minute / 60
#     df['Semana'] = df['Data Venda'].dt.isocalendar().week
#     df["Período"] = "1 - Manhã"
#     df.loc[df["Data Venda"].dt.hour >= 11, ["Período"]] = "2 - Almoço"
#     df.loc[df["Data Venda"].dt.hour >= 14, ["Período"]] = "3 - Tarde"
#     df.loc[df["Data Venda"].dt.hour >= 18, ["Período"]] = "4 - Noite"
#     return df

# @st.cache_data
# def read_delivery_data(filename):
#     print("Processing ", filename)
#     df = pd.read_excel(filename, skiprows=3, usecols=[10,12])
#     df.drop(df.tail(1).index, inplace=True)
#     df.rename(columns={"Numero Venda":"Número venda"}, inplace=True)
#     return df

# new_data = pd.read_csv("https://raw.githubusercontent.com/samirarman/gcm-data-center/main/sales.csv?token=GHSAT0AAAAAACP6YXXJB6IX454ERXJK6UDMZQDIVLQ")#pd.concat([read_data(file) for file in reports])
# data = new_data
data = pd.read_csv("data/sales.csv")
# data = new_data.merge(cat, on='Produto', how='left')
# delivery = pd.concat([read_delivery_data(file) for file in delivery_reports])
# data = data.merge(delivery, on='Número venda', how='left')
# data['Plataforma'].fillna("Presencial", inplace=True)
# data['Frappe do dia'] = False
# data.loc[data['Produto'] == 'FRAPPE DO DIA - P', 'Frappe do dia'] = True
# data.loc[(data['Produto'] == 'FRAPPE DO DIA - P') & (data['Dia da Semana'] == 1), 'Produto'] = 'FRAPPE VANILLA MACCHIATO - P'
# data.loc[(data['Produto'] == 'FRAPPE DO DIA - P') & (data['Dia da Semana'] == 2), 'Produto'] = 'FRAPPE CAPPUCCINO - P'
# data.loc[(data['Produto'] == 'FRAPPE DO DIA - P') & (data['Dia da Semana'] == 3), 'Produto'] = 'FRAPPE BANOFFEE - P'
# data.loc[(data['Produto'] == 'FRAPPE DO DIA - P') & (data['Dia da Semana'] == 4), 'Produto'] = 'FRAPPE RED - P'
# data.loc[(data['Produto'] == 'FRAPPE DO DIA - P') & (data['Dia da Semana'] == 5), 'Produto'] = 'FRAPPE CARAMEL - P'
datasets_tab.subheader("Sales Data")
datasets_tab.write(data)

montly_revenue = data.groupby(['Ano Mês'])['Total'].sum().reset_index()
# monthly_delivery_revenue = data[data['Plataforma'] != "Presencial"].groupby(['Ano Mês'])['Total'].sum().reset_index()
# monthly_delivery_revenue['Share'] = monthly_delivery_revenue['Total']/montly_revenue['Total'] * 100
# datasets_tab.subheader("Monthly delivery revenue")
# datasets_tab.write(monthly_delivery_revenue)

# monthly_delivery_by_platform = data[data['Plataforma'] != 'Presencial'].groupby(['Ano Mês', 'Plataforma'])['Total'].sum().reset_index()
# datasets_tab.subheader("Delivery by platform")
# datasets_tab.write(monthly_delivery_by_platform.merge(monthly_delivery_revenue, on='Ano Mês', how='left'))

# delivery_share = (100*data.groupby(['Ano Mês', 'Plataforma'])['Total'].sum()/data.groupby([ 'Ano Mês'])['Total'].sum()).reset_index()

datasets_tab.subheader("Got no idea what this is")
datasets_tab.write(data.groupby('Ano Mês')['Total'].count().reset_index())

monthly_rev = data.groupby(by="Ano Mês")["Total"].sum().reset_index()
monthly_rev_wd = data[data['Dia da Semana'] != 5].groupby(['Ano Mês'])["Total"].sum().reset_index()
monthly_rev_we = data[data['Dia da Semana'] == 5].groupby(['Ano Mês'])["Total"].sum().reset_index()
work_days = data.groupby(by="Ano Mês")["Data"].nunique().reset_index()
work_days_weekdays = data[data["Dia da Semana"] != 5].groupby(by="Ano Mês")["Data"].nunique().reset_index()
work_days_weekends = data[data["Dia da Semana"] == 5].groupby(by="Ano Mês")["Data"].nunique().reset_index()
work_days = work_days.merge(work_days_weekdays, how="right", on="Ano Mês")
work_days = work_days.merge(monthly_rev, on="Ano Mês", how="right")
work_days = work_days.merge(monthly_rev_wd, on="Ano Mês", how="right")
work_days = work_days.merge(monthly_rev_we, on="Ano Mês", how = "right")
work_days = work_days.rename(columns={"Data_x":"Dias trabalhados", "Data_y":"Dias de semana", "Total_x":"Total", "Total_y":"Total dias de semana", "Total": "Total sábados"})

work_days["Sábados"] = work_days["Dias trabalhados"] - work_days["Dias de semana"]
work_days["Receita média dias de semana"] = work_days["Total dias de semana"] / work_days["Dias de semana"]
work_days["Receita média sábados"] = work_days["Total sábados"] / work_days["Sábados"]

day_period = data.groupby(['Ano Mês', 'Período'])['Total'].sum().reset_index().merge(monthly_rev, how='right', on='Ano Mês')
day_period["Percentual"] = day_period["Total_x"]/day_period["Total_y"] * 100

share = data.groupby(['Ano Mês', 'Número venda'])['Quantidade'].sum().reset_index()
share['Quantidade'] = share['Quantidade'].astype('int')
share = share.groupby([ 'Ano Mês','Quantidade']).count()['Número venda'].reset_index().merge(share.groupby([ 'Ano Mês']).count()['Quantidade'].reset_index(), on='Ano Mês', how='left')
share['Percentage'] = share['Número venda']/share['Quantidade_y'] * 100

ldm = pd.read_csv("aux_data/ldm.csv")#pd.read_sql_query("SELECT * FROM boms_view", con)
datasets_tab.subheader("LDM")
datasets_tab.write(ldm)

# purchases = pd.read_sql_query("SELECT * FROM excel_exporter", con, parse_dates=True)
# purchases = purchases.iloc[:,[0,2,11,12,13,14,15,16,17,19,]].set_axis(['date', 'material', 'price', 'disc', 'freight', 'icms_st', 'difal', 'ipi', 'total', 'qty'], axis=1)
# purchases['unit_price'] = purchases['price']/purchases['qty']
# purchases['unit_cost'] = purchases['total']/purchases['qty']
# purchases['surcharge'] = purchases['total']/purchases['price'] - 1
# purchases['date'] = pd.to_datetime(purchases['date'])
# purchases['year_month'] = purchases['date'].dt.strftime('%Y-%m')
purchases = pd.read_csv("aux_data/purchases.csv")
datasets_tab.write(purchases)

avg_cost = purchases.groupby(['year_month','material'])[['total', 'qty']].sum().reset_index()
avg_cost['avg_cost'] = avg_cost['total']/avg_cost['qty']
materials = ldm['material_id'].unique()

def fill_avg_costs(material):
    a = avg_cost[avg_cost['material'] == material]
    lh = purchases['year_month'].drop_duplicates().reset_index().sort_values(by='year_month')
    return lh.merge(a, on='year_month', how='left').ffill()
    
avg_cost = pd.concat([fill_avg_costs(material) for material in materials])   
datasets_tab.subheader("Average cost")
datasets_tab.write(avg_cost)


    

products = data['Produto'].unique()
qty_sold = data.groupby(["Ano Mês", "Produto"])[['Total', 'Quantidade']].sum().reset_index()
datasets_tab.subheader('Product qty and revenue overview')
datasets_tab.write(qty_sold)

@st.cache_data
def calculate_cogs(product):
    df = pd.DataFrame()
    materials = ldm[ldm['product_id'] == product]['material_id'].unique()
  
    if len(materials) != 0:
        for material in materials:
            unit_qty = ldm[(ldm['product_id'] == product) & (ldm['material_id'] == material)].tail(1).reset_index().loc[0,'qty']
            new_df = pd.DataFrame()
            new_df['year_month'] = avg_cost['year_month'].unique()
            filtered_data = avg_cost[avg_cost['material'] == material]
            new_df = new_df.merge(filtered_data, on = 'year_month', how='left')
            new_df['material_cost'] = unit_qty * new_df['avg_cost']
            new_df['unit_qty'] = unit_qty
            new_df['product'] = product
            df = pd.concat([df, new_df])
    
    return df 

datasets_tab.subheader('Material cost for recipe')    
material_usage = pd.concat([calculate_cogs(product) for product in products])
datasets_tab.write(material_usage)
product_cost = material_usage.groupby(['product', 'year_month'])['material_cost'].sum().reset_index()
datasets_tab.subheader('Product cost evolution')
datasets_tab.write(product_cost)

datasets_tab.subheader("TESTE TESTE")
data = data.merge(product_cost, left_on=['Ano Mês', 'Produto'], right_on=['year_month', 'product'], how='left')
data['nominal_cost'] = data['Quantidade'] * data['material_cost']
datasets_tab.write(data)

qty_sold = qty_sold.merge(product_cost, left_on=['Ano Mês', 'Produto'], right_on=['year_month', 'product'], how='left')
qty_sold['avg_price'] = qty_sold['Total'] / qty_sold['Quantidade']
qty_sold['nominal_cost'] = qty_sold['Quantidade'] * qty_sold['material_cost']
qty_sold['gross_margin'] = qty_sold['Total'] - qty_sold['nominal_cost']
qty_sold['net_margin'] = qty_sold['Total'] * 0.9225 - qty_sold[ 'nominal_cost']
qty_sold[ 'unit_net_margin'] = qty_sold['net_margin'] / qty_sold['Quantidade']
qty_sold['gross_cogs_perc'] = qty_sold['material_cost'] / qty_sold['avg_price']
qty_sold['net_cogs_perc'] = qty_sold['material_cost'] / (qty_sold['avg_price'] * 0.9225)
qty_sold['ideal_price_26'] = qty_sold['material_cost'] / 0.28
qty_sold['ideal_price_30'] = qty_sold['material_cost'] / 0.30

datasets_tab.subheader("Qty Sold dataset")
datasets_tab.write(qty_sold)

#####################
# KPI TAB
#####################

kpi_tab.subheader("Revenue")
kpi_tab.line_chart(data.groupby('Data')['Total'].sum().reset_index().rename(columns={"Total":"Receita"}), x='Data', y='Receita')
kpi_tab.bar_chart(data.groupby(['Ano Mês'])['Total'].sum().reset_index().rename(columns={"Total":"Receita"}), x='Ano Mês', y='Receita')
kpi_tab.line_chart(data.groupby(['Ano', 'Semana'])['Total'].sum().reset_index().rename(columns={"Total":"Receita"}), x='Semana', y='Receita', color='Ano')
# kpi_tab.line_chart(data.groupby(['Ano', 'Mês'])['Total'].sum().reset_index().rename(columns={"Total":"Receita"}), x='Mês', y='Receita', color='Ano')
kpi_tab.subheader('Quantidade de produtos por pedido')
kpi_tab.line_chart(share, y='Percentage', x='Ano Mês', color='Quantidade_x')

kpi_tab.subheader("Average revenue on weekday types")
kpi_tab.line_chart(work_days,x = "Ano Mês", y="Receita média dias de semana")
kpi_tab.line_chart(work_days,x = "Ano Mês", y="Receita média sábados")
kpi_tab.line_chart(day_period, x = "Ano Mês", y = "Percentual", color = "Período")

kpi_tab.subheader("Delivery analysis")
# kpi_tab.line_chart(monthly_delivery_by_platform, x='Ano Mês', y='Total', color='Plataforma')
# kpi_tab.line_chart(delivery_share.rename(columns={"Total":"Share"}), x="Ano Mês", y="Share", color="Plataforma")

month_choices = pd.Series(qty_sold['Ano Mês'].unique()).sort_values()
sel_month = kpi_tab.selectbox("Selecione um mês:", month_choices, index=len(month_choices) - 1)
category_choice = kpi_tab.checkbox("Por Categoria?")
filtered_frame = qty_sold[qty_sold['Ano Mês'] == sel_month].reset_index()
if category_choice:
    print(filtered_frame)
    filtered_frame = filtered_frame.groupby('Categoria')['net_margin, Quantidade'].sum()
kpi_tab.scatter_chart(filtered_frame, x= "Quantidade", y="net_margin", color="product")


#####################
# COGS TAB
#####################

cogs_tab.write(qty_sold[qty_sold['Ano Mês'] == '2024-02'][['Produto', 'material_cost', 'avg_price', 'ideal_price_26', 'ideal_price_30']])
sel_prod = cogs_tab.selectbox("Selecione um produto:", pd.Series(data['Produto'].unique()).sort_values())
cogs_tab.subheader(sel_prod)
filtered_product = qty_sold[qty_sold['Produto'] == sel_prod]
filtered_material = material_usage[material_usage['product'] == sel_prod]
filtered_ldm = ldm[ldm['product_id'] == sel_prod]

cogs_tab.line_chart(filtered_product, x= 'Ano Mês', y='Total')
cogs_tab.line_chart(filtered_product, x='Ano Mês', y='Quantidade')
cogs_tab.line_chart(filtered_product, x= 'Ano Mês', y= 'net_margin')
cogs_tab.line_chart(filtered_product, x='Ano Mês', y='gross_cogs_perc')
cogs_tab.line_chart(filtered_product, x='Ano Mês', y='net_cogs_perc')
cogs_tab.line_chart(filtered_product, x='year_month', y='material_cost')
cogs_tab.line_chart(filtered_material, x='year_month', y='material_cost', color='material')
cogs_tab.line_chart(filtered_product, x='Ano Mês', y=['ideal_price_26', 'ideal_price_30', 'avg_price'])
cogs_tab.write(filtered_ldm)

#####################
# MATERIAL TAB
#####################


material_tab.subheader("Material cost evolution")
sel_material = material_tab.selectbox("Selecione um insumo:", pd.Series(purchases['material'].unique()).sort_values())
material_data = purchases[purchases['material'] == sel_material]
datasets_tab.write(material_data)
datasets_tab.write(avg_cost)

material_tab.line_chart(material_data, x='date', y='unit_cost')
material_tab.line_chart(material_data, x='date', y='unit_price')
material_tab.line_chart(material_data, x='date', y= 'surcharge')
avg_material_data = avg_cost[avg_cost['material'] == sel_material]
material_tab.line_chart(avg_material_data, x='year_month', y='avg_cost')


#####################
# INVENTORY TAB
#####################
prod_data = pd.read_csv("aux_data/prod_data.csv")
# moves = pd.read_csv("../moves.csv")
inventory_tab.subheader("Materials levels")
inv_demand = pd.read_csv("data/inventory_demand.csv")
inventory = inv_demand.merge(prod_data, on="Produto", how="left")

datasets_tab.write(inv_demand)
datasets_tab.write(prod_data)
inventory = inventory[inventory["Descontinuado"] == "Não"]
inventory['Estoque alvo'] = -inventory["Demanda"] * (inventory["Período"] + inventory["Lead"]) + -inventory["Demanda"] * inventory["Segurança"]
inventory["Necessidade"] = inventory["Estoque alvo"] - inventory["Saldo"]
inventory.loc[inventory["Necessidade"] <= 0, "Necessidade"] = 0
inventory["Pedido"] = np.ceil(inventory["Necessidade"]/inventory["Embalagem"])
inventory["Custo"] = inventory["Pedido"] * inventory["Preço"]
datasets_tab.write(inventory)

inventory_tab.subheader("Níveis")
inventory_tab.dataframe(data=inventory[inventory["Pedido"] > 0][['Produto', 'Saldo']])

inventory_tab.subheader("Pedidos")
inventory_tab.dataframe(data=inventory[inventory["Pedido"] > 0].groupby(['Lista', 'Produto'])[['Pedido', 'Custo']].sum().reset_index().style.format({"Custo": "${:,}"}),)

inventory_tab.subheader("Valor do pedido de cada lista")
inventory_tab.dataframe(data=inventory[inventory["Pedido"] > 0].groupby(['Lista'])['Custo'].sum().reset_index().style.format({"Custo": "${:,}"}),)
# inventory_tab.subheader("Discrepâncias nas fichas técnicas")
# inventory_tab.write(moves[['Produto', 'Ajuste %']].sort_values('Ajuste %'))

# inventory_tab.subheader("Perdas Documentadas")
# inventory_tab.write(moves[['Produto', 'Perda %']].sort_values('Perda %', ascending=False))