import time
import textblob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https:/google.com/gmail"

# Start Safari
driver = webdriver.Chrome('./chromedriver')
driver.get(URL)


def log_in(usernm, passwrd):
    """Function for loggin in on gmail"""
    # Insert Username/Password
    username = driver.find_element_by_name('identifier')
    username.clear()
    username.send_keys(usernm)

    # Submit the username
    username.send_keys(Keys.RETURN)

    find_element_presence(15, By.NAME, 'password')

    # Replace ### with the actual password
    password = driver.find_element_by_name('password')
    password.clear()
    password.send_keys(passwrd)

    # Submit the form
    password.send_keys(Keys.RETURN)

# Function for finding elements on page


def find_element_presence(timeout, by, path):
    """Function for finding if an element is present in the actual DOM."""
    element_present = EC.presence_of_element_located((by, path))
    WebDriverWait(driver, timeout).until(element_present)


log_in('demobtss20@gmail.com', '&cY1H(91=G-&')

find_element_presence(20, By.XPATH, '//tr[@role="row"]')
emails = driver.find_elements_by_xpath('//tr[@role="row"]')


def convert_polarity(polarity):
    if polarity < 0.1 and polarity > -0.1:
        return 'neutral'
    elif polarity >= 0.1:
        return 'positive'
    elif polarity <= 0.1:
        return 'negative'


feedback = ""
for email in emails:
    time.sleep(0.45)
    email.click()

    find_element_presence(10, By.XPATH, '//h2[@class="hP"]')
    feedback += 'Email: ' + \
        driver.find_element_by_xpath('//h2[@class="hP"]').text + '\n'

    content = driver.find_element_by_xpath('//div[@class="ii gt"]').text
    blob = textblob.TextBlob(content)

    avg_polarity = 0
    avg_subjectivity = 0
    for idx, sentence in enumerate(blob.sentences):
        avg_polarity += sentence.sentiment.polarity
        avg_subjectivity += sentence.sentiment.subjectivity
        feedback += f'\tSentence {idx+1}: \n\t\tSentiment: {convert_polarity(sentence.sentiment.polarity)}\n\t\tSubjectivity: {sentence.sentiment.subjectivity}\n'

    feedback += f'\n\tAverage polarity {avg_polarity/len(blob.sentences)} - {convert_polarity(avg_polarity/len(blob.sentences))}\n'
    feedback += f'\tAverage subjectivity {avg_subjectivity/len(blob.sentences)}\n'

    feedback += '-'*6 + '\n'

    driver.back()

print(feedback)

# Close the driver
driver.close()
