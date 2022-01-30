from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from pymongo import MongoClient
import login_pswd_data
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

db = MongoClient('localhost', 27017)['mail_ru']
collection = db.mail_messages

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

email = login_pswd_data.email
password = login_pswd_data.password

driver = webdriver.Chrome(options=chrome_options)
data_letters = []
msg_links = set()
data_list = []
msg_count = 0


def parse_messages():
    for url_msg in msg_links:
        driver.get(url_msg)
        try:
            date = driver.find_element(By.CLASS_NAME, 'letter__date').text
            subject = driver.find_element(By.XPATH, "//h2[@class='thread-subject']").text
            sender_name = driver.find_element(By.CLASS_NAME, 'letter-contact').text
            sender_email = driver.find_element(By.CLASS_NAME, 'letter-contact').get_attribute('title')
            message_text = driver.find_element(By.CLASS_NAME, 'letter__body').text.strip().replace('\n', '.')
            data_list.append({
                'date': date,
                'subject': subject,
                'sender_name': sender_name,
                'sender_email': sender_email,
                'message_text': message_text
            })
        except Exception as ex:
            print(ex)


try:
    driver.get('https://mail.ru/')
    emal_input = driver.find_element(By.NAME, 'login')
    emal_input.clear()
    emal_input.send_keys(email)
    enter_pasword_btn = driver.find_element(By.XPATH, "//button[@data-testid='enter-password']")
    enter_pasword_btn.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)
    input_password = driver.find_element(By.XPATH, "//*[@type='password']")
    input_password.clear()
    input_password.send_keys(password)
    input_password.send_keys(Keys.ENTER)
    msg_driver = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'dataset__items')))
    messages = msg_driver.find_elements(By.TAG_NAME, 'a')

    while True:
        length = len(msg_links)
        for message in messages:
            link = message.get_attribute('href')
            try:
                if 'e.mail' in link:
                    msg_links.add(link)
            except Exception as ex:
                print(ex)
        try:
            action = ActionChains(driver)
            action.move_to_element(messages[-1])
            action.perform()
            msg_driver = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'dataset__items')))
            messages = msg_driver.find_elements(By.TAG_NAME, 'a')
        except Exception as ex:
            print(ex)
        if length == len(msg_links):
            print(msg_links)
            break
    msg_count += 1
    parse_messages()

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

db.collection.insert_many(data_list)
