from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time
from datetime import date
import sys

IMPLICIT_WAIT = 120
ACTION_WAIT = 15
DOWNLOAD_WAIT = 120

user = sys.argv[1]
key = sys.argv[2]

if "--debug" in sys.argv:
    DEBUG = True
else:
    DEBUG = False

if "--no-headless" in sys.argv:
    HEADLESS = False
else:
    HEADLESS = True


def act_wait():
    time.sleep(ACTION_WAIT)

def initial_date():
    return date.today().replace(day=1).strftime("%d/%m/%Y")

def final_date():
    return date.today().strftime("%d/%m/%Y")

def setup_driver():

    chrome_service = Service()#ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    chrome_options = Options()

    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=2560,1920",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--remote-debugging-pipe",
    ]

    if HEADLESS is False:
        options.remove("--headless")

    for option in options:
        chrome_options.add_argument(option)


    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.implicitly_wait(IMPLICIT_WAIT)

    return driver


def navigate_to_home(driver:webdriver.Chrome):
    driver.get("https://app2.controlenamao.com.br/#!/login")

    if DEBUG:
        print(driver.page_source)


def login(driver:webdriver.Chrome):
    username = driver.find_element(By.ID, "emailLogin")
    password = driver.find_element(By.ID, "senhaLogin")
    login_button = driver.find_element(By.ID, "btnCadastroEmpresa")
    username.send_keys(user)
    password.send_keys(key)
    login_button.click()

    act_wait()

    try:
        use_here_button = driver.find_element(By.CLASS_NAME, 'confirm')
        use_here_button.click()
        act_wait()
        if DEBUG:
            act_wait()
            print(driver.page_source)
    except Exception:
        pass


def navigate_to_sales_report(driver:webdriver.Chrome):
    driver.get("https://app2.controlenamao.com.br/#!/relatorio/venda")
    if DEBUG:
        act_wait()
        print(driver.page_source)

def retrive_form_elements(driver:webdriver.Chrome):
    #Find form elements for sales report options
    options_form = driver.find_element(By.TAG_NAME, 'form')
    options_form_inputs = options_form.find_elements(By.TAG_NAME, "input")
    options_form_buttons = options_form.find_elements(By.TAG_NAME, "button")

    initial_date_field = options_form_inputs[0]
    final_date_field = options_form_inputs[3]

    filter_button = options_form_buttons[0]
    apply_filter_button = options_form_buttons[1]

    return {"initial_date_field":initial_date_field,
            "final_date_field":final_date_field,
            "filter_button":filter_button,
            "apply_filter_button":apply_filter_button,
            }


def fill_filter_form(elements:dict[str, webdriver.remote.webelement]):
    # Fill in form elements
    elements["initial_date_field"].clear()
    elements["initial_date_field"].send_keys(initial_date())

    elements["final_date_field"].clear()
    elements["final_date_field"].send_keys(final_date())

    act_wait()


def setup_sales_report(driver:webdriver.Chrome):

    form_elements = retrive_form_elements(driver)
    fill_filter_form(form_elements)
    form_elements["filter_button"].click()
    act_wait()
    
    # Fill-in sales report options
    options_container = driver.find_element(By.ID, "sidebarFiltrosRelatorioVendasElement")
    report_options = options_container.find_element(By.ID, "cbTipoAgrupamento_chosen")
    report_options.click()
    act_wait()

    option_text_container = options_container.find_element(By.CLASS_NAME, "chosen-search")
    option_text_input = option_text_container.find_element(By.TAG_NAME, "input")
    option_text_input.send_keys("Detalhado")
    option_text_input.send_keys(Keys.ENTER)
    act_wait()

    arrow_button = driver.find_element(By.CLASS_NAME, "closebtn")
    arrow_button.click()
    act_wait()

    # Generate the report
    form_elements["apply_filter_button"].click()
    act_wait()

    if DEBUG:
        print(driver.page_source)


def navigate_to_inventory_report(driver:webdriver.Chrome):
    driver.get("http://app2.controlenamao.com.br/#!/relatorio/estoque")
    if DEBUG:
        act_wait()
        print(driver.page_source)


def setup_inventory_report(driver:webdriver.Chrome):

    form_elements = retrive_form_elements(driver)
    fill_filter_form(form_elements)
    form_elements["filter_button"].click() 
    act_wait()
    
    options_container = driver.find_element(By.ID, 'sidebarFiltrosRelatorioEstoqueElement')
    report_options = options_container.find_element(By.ID, 'cbtipoAgrupamento_chosen')
    report_options.click()
    act_wait()

    option_text_container = options_container.find_element(By.CLASS_NAME, 'chosen-search')
    options_text_input = option_text_container.find_element(By.TAG_NAME, 'input')
    options_text_input.send_keys("Detalhadas")
    options_text_input.send_keys(Keys.ENTER)
    act_wait()

    arrow_button = driver.find_element(By.CLASS_NAME, 'closebtn')
    arrow_button.click()
    act_wait()

    form_elements["apply_filter_button"].click()
    act_wait()

    
def download_report(driver:webdriver.Chrome):
    download_button = driver.find_element(By.ID, "btnExport")
    download_button.click()
    time.sleep(DOWNLOAD_WAIT)
    

def main():
    print("Setting-up Chrome browser")
    with setup_driver() as driver:
        act_wait()

        print("Navigating to home page")
        navigate_to_home(driver)
        act_wait()

        print("Logging into application")
        login(driver)
        act_wait()

        print("Accessing sales report")
        navigate_to_sales_report(driver)
        act_wait()

        print("Setting-up sales report")
        setup_sales_report(driver)
        act_wait()

        print("Downloading sales report")
        download_report(driver)
        act_wait()

        #print("Accessing inventory report")
        #navigate_to_inventory_report(driver)
        #act_wait()

        #print("Setting-up inventory report options")
        #setup_inventory_report(driver)
        #act_wait()

        #print("Downloading inventory report")
        #download_report(driver)
        #act_wait()

if __name__ == "__main__":
    main()
