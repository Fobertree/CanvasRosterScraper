from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
import os
from dotenv import load_dotenv
from math import ceil
import numpy as np

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


start = time.time()

headless_mode = False

website = os.getenv('WEBSITE')
path = os.getenv("PATH")

dest_path = "Roster"

webdriver_service = Service(path)
chrome_options = Options()

if headless_mode:
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')

driver = webdriver.Chrome(service = webdriver_service,options = chrome_options)

driver.get(website)

wait = WebDriverWait(driver,20)

# Login

wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(username)
wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))).click()
print("Logged in")

names = []
first_names = []
last_names = []

for _ in tqdm(range(ceil(955/25))): #we have 955 students. This is naturally an upper bound and will go through more iterations than necessary
    driver.execute_script("window.scroll(0,document.body.scrollHeight);") #scroll entire website to load elements
    wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(@class, 'roster_user_name')]")))

containers = driver.find_elements(by=By.XPATH,value = "//*[contains(@class, 'roster_user_name')]")

for container in containers:
    name = container.text
    names.append(name)
    name = name.split(" ")
    first_names.append(name[0])
    last_names.append(name[-1])

print(names)
print(len(containers),len(names))

# convert to csv

rows = []

for _ in range(len(names)):
    rows.append([names.pop(),first_names.pop(),last_names.pop()])

np.savetxt("Roster.csv",rows,delimiter=", ",fmt="% s")

print(f'{time.time()-start:.2f} seconds')

driver.quit()
