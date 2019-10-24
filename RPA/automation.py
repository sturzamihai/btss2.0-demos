import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https:/google.com/gmail"

# Start Safari
driver = webdriver.Safari()
driver.get(URL)

# Insert Username/Password
username = driver.find_element_by_name('identifier')
username.clear()
username.send_keys('demobtss20@gmail.com')

# Submit the username
username.send_keys(Keys.RETURN)

# Wait until we can input the password
element_present = EC.presence_of_element_located((By.NAME, 'password'))
WebDriverWait(driver, 15).until(element_present)

password = driver.find_element_by_name('password') # Replace ### with the actual password
password.clear()
password.send_keys('#####')

# Submit the form
password.send_keys(Keys.RETURN)

# Wait until 'Compose' button shows up then click on it
element_present = EC.presence_of_element_located((By.XPATH, '//div[contains(text(),\'Compose\')]'))
WebDriverWait(driver, 15).until(element_present)

# Selenium bad >:(
driver.find_element_by_xpath('//div[contains(text(),\'Compose\')]').click() # New ideea - select first email from inbox and make stats like subjectivity/sentiment of the content

# Close the driver
driver.close()