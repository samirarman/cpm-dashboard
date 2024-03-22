from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time
from datetime import date
import sys

print("Script starting")
WAIT = 60

user = sys.argv[1]
key = sys.argv[2]

def initial_date():
    return "01/03/2024"

def final_date():
    return date.today().strftime("%d/%m/%Y")

# chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=2560,1920",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

print("Starting Chrome")
driver = webdriver.Chrome(options=chrome_options)

driver.implicitly_wait(WAIT)
driver.get("https://app2.controlenamao.com.br/#!/login")
print(driver.title)

username = driver.find_element(By.ID, "emailLogin")
password = driver.find_element(By.ID, "senhaLogin")
login_button = driver.find_element(By.ID, "btnCadastroEmpresa")
username.send_keys(user)
password.send_keys(key)
login_button.click()

time.sleep(WAIT)

try:
    use_here_button = driver.find_element(By.CLASS_NAME, 'confirm')
    print(use_here_button.text)
    use_here_button.click()
except Exception:
    pass

time.sleep(WAIT)

# SALES REPORT
# ============
driver.get("https://app2.controlenamao.com.br/#!/relatorio/venda")
time.sleep(WAIT)
driver.save_screenshot("access.png")
print(driver.title)
# reports_button = driver.find_element(By.CLASS_NAME, 'relatorio-svg')
# reports_button.click()

# time.sleep(WAIT)
# sales_report = driver.find_element(By.PARTIAL_LINK_TEXT, 'Vendas')
# sales_report.click()


# options_form = driver.find_element(By.TAG_NAME, 'form')
# options_form_inputs = options_form.find_elements(By.TAG_NAME, "input")
# options_form_buttons = options_form.find_elements(By.TAG_NAME, "button")

# initial_date_field = options_form_inputs[0]
# final_date_field = options_form_inputs[3]

# filter_button = options_form_buttons[0]
# apply_filter_button = options_form_buttons[1]

# initial_date_field.clear()
# initial_date_field.send_keys(initial_date())

# final_date_field.clear()
# final_date_field.send_keys(final_date())

# time.sleep(WAIT)
# driver.save_screenshot("2.png")
# filter_button.click()

# options_container = driver.find_element(By.ID, "sidebarFiltrosRelatorioVendasElement")

# report_options = options_container.find_element(By.ID, "cbTipoAgrupamento_chosen")
# report_options.click()

# time.sleep(WAIT)


# option_text_container = options_container.find_element(By.CLASS_NAME, "chosen-search")
# option_text_input = option_text_container.find_element(By.TAG_NAME, "input")
# option_text_input.send_keys("Detalhado")
# option_text_input.send_keys(Keys.ENTER)

# time.sleep(WAIT)
# driver.save_screenshot("3.png")    

# arrow_button = driver.find_element(By.CLASS_NAME, "closebtn")
# arrow_button.click()
# time.sleep(WAIT)
# driver.save_screenshot("4.png")

# apply_filter_button.click()
# time.sleep(WAIT)

# driver.save_screenshot("5.png")

# download_button = driver.find_element(By.ID, "btnExport")
# download_button.is_enabled()
# download_button.click()

# time.sleep(120)
# driver.save_screenshot("6.png")
driver.quit()
