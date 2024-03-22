from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
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

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

print("Starting Chrome")
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)




print("Firefox started. Navigating to a page")
driver.get("https://www.google.com/")

print(driver.title)
driver.close()
