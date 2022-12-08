# libraries, packages, etc
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome("C:\Drivers\chromedriver\chromedriver.exe", chrome_options=chrome_options)

today = date.today()
d1 = today.strftime("%d/%m/%Y")

# Ukraine
driver.get("https://acleddata.com/data-export-tool/")
driver.find_element(By.NAME, "key").send_keys("972-Ilk48Q12S9w-fcri")
driver.find_element(By.NAME, "email").send_keys(r"jmeltze1@umd.edu")
driver.find_element(By.NAME, "event_date_from").send_keys(r"01/11/2020")
driver.find_element(By.NAME, "event_date_to").send_keys(d1)
driver.find_element(By.NAME, "country_typing").send_keys("Ukraine")
driver.find_element(By.XPATH, "//input[@data-check='mc-ukraine']").click()
driver.find_element(By.XPATH, "//button[normalize-space()='Accept']").click()
driver.find_element(By.XPATH, "//input[@value='Export']").click()