"""
Вариант I
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах
в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#
"""

from time import sleep

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# get driver
service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_argument("start-maximized")
options.add_argument("--blink-settings=imagesEnabled=false")
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(30)

# get url
driver.get("https://mail.ru/")

# login
elem = driver.find_element(By.NAME, "login")
elem.send_keys("study.ai_172")
elem.send_keys(Keys.ENTER)

# password
elem = driver.find_element(By.NAME, "password")
elem.send_keys("NextPassword172#")
elem.send_keys(Keys.ENTER)

# links collection
letter_urls = []
last_letter_url = ""

while True:
    sleep(3)
    elems = driver.find_elements(By.CSS_SELECTOR, "a.llc")
    urls = [elem.get_attribute("href").split("?")[0] for elem in elems]
    for url in urls:
        if url not in letter_urls:
            letter_urls.append(url)
    elems[-1].send_keys(Keys.PAGE_DOWN)
    if last_letter_url != urls[-1]:
        last_letter_url = urls[-1]
    else:
        break

# db params
client = MongoClient("127.0.0.1", 27017)
db = client["letters"]
letters = db.letters

for url in letter_urls:
    driver.get(url)
    driver.implicitly_wait(30)
    sender = driver.find_element(By.XPATH, "//div[@class='letter__author']/span")
    date = driver.find_element(By.XPATH, "//div[@class='letter__date']")
    title = driver.find_element(By.XPATH, "//h2[@class='thread-subject']")
    text = driver.find_elements(By.XPATH, "//div[@class='html-expander']//td/*")
    text_lst = [p.text for p in text if p.text]
    document = {
        "from": sender.get_attribute("title"),
        "date": date.text,
        "title": title.text,
        "text": "".join(text_lst),
    }

    letters.insert_one(document)
