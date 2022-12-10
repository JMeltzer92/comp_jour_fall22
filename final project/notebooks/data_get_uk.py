# libraries, packages, etc
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

chrome_options = Options()
prefs = {'download.default_directory' : r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data'}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(r"drivers\chromedriver\chromedriver.exe", chrome_options=chrome_options)

today = date.today()
d1 = today.strftime("%d/%m/%Y")

# download csv
driver.get("https://acleddata.com/data-export-tool/")
driver.find_element(By.NAME, "key").send_keys("972-Ilk48Q12S9w-fcri")
driver.find_element(By.NAME, "email").send_keys(r"jmeltze1@umd.edu")
driver.find_element(By.NAME, "event_date_from").send_keys(r"01/11/2020")
driver.find_element(By.NAME, "event_date_to").send_keys(d1)
driver.find_element(By.NAME, "country_typing").send_keys("Ukraine")
driver.find_element(By.XPATH, "//input[@data-check='mc-ukraine']").click()
driver.find_element(By.XPATH, "//button[normalize-space()='Accept']").click()
driver.find_element(By.XPATH, "//input[@value='Export']").click()

# wait for download
time.sleep(10)

# remove old file
os.remove(r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data\ukr.csv')

# rename new file
ukraine = [i for i in os.listdir(r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data') if i.endswith('Ukraine.csv')]
old_file = os.path.join(r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data', ukraine[0])
new_file = os.path.join(r'C:\Users\Jon\Documents\GitHub\comp_jour_fall22\final project\data', 'ukr.csv')
os.rename(old_file, new_file)