from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from pymongo import MongoClient

db = MongoClient('localhost', 27017)['Mvideo']
collection = db.hits

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)
data = []


try:
    driver.get('https://www.mvideo.ru/')
    hits = driver.find_element(By.XPATH, '//mvid-product-cards-group')
    action = ActionChains(driver)
    action.move_to_element(hits)
    action.perform()
    names = driver.find_elements(By.XPATH, '//*[contains(@class, "product-mini-card__name")]')
    price = driver.find_elements(By.XPATH, '//*[contains(@class, "product-mini-card__price")]')
    for i in range(0, len(names)):
        data.append({
            'name': names[i].text,
            'price': price[i].text.split('\n')[0],
            'link': names[i].find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'a').get_attribute('href')
        })

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


print(data)

db.collection.insert_many(data)
