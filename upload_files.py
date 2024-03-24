import pathlib
import dropbox
from dropbox.exceptions import AuthError, ApiError
from dropbox.files import WriteMode
import sys
from glob import glob

if len(sys.argv) != 4:
    print("No access token provided")
    exit()

DBX_APP_KEY = sys.argv[1]
DBX_APP_SECRET = sys.argv[2]
DBX_REFRESH_TOKEN = sys.argv[3]

def dropbox_connect():
    dbx = dropbox.Dropbox(app_key=DBX_APP_KEY,
                              app_secret=DBX_APP_SECRET,
                              oauth2_refresh_token=DBX_REFRESH_TOKEN)
    try:
        dbx.users_get_current_account()
    except AuthError as e:
        print('Error connecting to Dropbox:' + str(e))
    return dbx

dbx = dropbox_connect()
print("Connection to Dropbox successfull!")

# def list_files(files):
#     for file in files.entries:
#         print(file.name)
        
        
# files = dbx.files_list_folder('/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Venda')
# print("Found the following files:")
# list_files(files)


# print("Downloading sales reports files")
# dbx.files_download_zip_to_file("Vendas.zip",'/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Venda')
# print("Sales reports files download complete")

# files = dbx.files_list_folder('/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Estoque Detalhado')
# print("Found the following files:")
# list_files(files)

# print("Downloading stock reports files")
# dbx.files_download_zip_to_file("EstoqueDetalhado.zip", '/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Estoque Detalhado')
# print("Stock reports files download complete")



# LOCALFILE = "/Users/samir/Downloads/Reports/Relatorio_2024_03.xls"

# BACKUPPATH ='/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Estoque Detalhado' + '/Relatorio_2024_03.xls'

def upload_file(filename):
    if "Estoque" in filename:
        backup_path ='/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Estoque Detalhado/' + filename
    else:
        backup_path='/Projeto GoCoffee/Financeiro/Relatórios do sistema/Relatórios de Venda/' + filename
    with open(filename, 'rb') as f:
            # We use WriteMode=overwrite to make sure that the settings in the file
            # are changed on upload
            print("Uploading " + filename + " to Dropbox as " + backup_path + "...")
            try:
                dbx.files_upload(f.read(), backup_path, mode=WriteMode('overwrite'))
            except ApiError as err:
                # This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
                if (err.error.is_path() and
                        err.error.get_path().error.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)
                    sys.exit()
def main():
    filelist = glob("*.xls")               
    for file in filelist:
        upload_file(file)
    
if __name__ == '__main__':
    main()