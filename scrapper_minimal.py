from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

print("Starting Firefox")
driver = webdriver.Firefox(options=firefox_options)
driver.implicitly_wait(WAIT)

print("Firefox started. Navigating to a page")
driver.get("https://www.google.com/")

print(driver.title)
driver.close()
