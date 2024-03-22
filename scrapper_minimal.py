from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date
import sys

WAIT = 10

user = sys.argv[1]
key = sys.argv[2]

def initial_date():
    return "01/03/2024"

def final_date():
    return date.today().strftime("%d/%m/%Y")

firefox_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--width=2560",
    "--height=1920",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    firefox_options.add_argument(option)
    
driver = webdriver.Firefox(options=firefox_options)
driver.implicitly_wait(WAIT)
driver.get("https://app2.controlenamao.com.br/#!/login")
print(driver.title)
driver.close()
