from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https:/sturzamihai.com/webmail"

# Start Safari
driver = webdriver.Safari()
driver.get(URL)

# Wait until cPanels connects to the mailbox
timeout = 60
element_present = EC.presence_of_element_located((By.NAME, 'user'))
WebDriverWait(driver, timeout).until(element_present)

# Insert Username/Password
username = driver.find_element_by_name("user")
username.clear()
username.send_keys("test@sturzamihai.com")

password = driver.find_element_by_name("pass") # Replace ### with the actual password
password.clear()
password.send_keys("###")

# Submit the form
password.send_keys(Keys.RETURN)

# Will implement mail sending logic

driver.close()