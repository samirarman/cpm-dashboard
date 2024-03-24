import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError
import sys

if len(sys.argv) != 4:
    print("No access token provided")
    exit()

DBX_APP_KEY = sys.argv[1]
DBX_APP_SECRET = sys.argv[2]
DBX_REFRESH_TOKEN = sys.argv[3]

def dropbox_connect():
    try:
        dbx = dropbox.Dropbox(app_key=DBX_APP_KEY,
                              app_secret=DBX_APP_SECRET,
                              oauth2_refresh_token=DBX_REFRESH_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox:' + str(e))
    return dbx

dbx = dropbox_connect()
print("Connection to Dropbox successfull!")

def list_files(files):
    for file in files.entries:
        print(file.name)
        
        
files = dbx.files_list_folder('/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Venda')
print("Found the following files:")
list_files(files)


print("Downloading sales reports files")
dbx.files_download_zip_to_file("Vendas.zip",'/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Venda')
print("Sales reports files download complete")

files = dbx.files_list_folder('/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Estoque Detalhado')
print("Found the following files:")
list_files(files)

print("Downloading stock reports files")
dbx.files_download_zip_to_file("EstoqueDetalhado.zip", '/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Estoque Detalhado')
print("Stock reports files download complete")
