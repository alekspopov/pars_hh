import os
import time
import json
import csv
from operator import index

from selenium import webdriver
from unicodedata import digit
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
chrome_options.add_argument("--window-size=1280,700")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 30, poll_frequency=1)
action = ActionChains(driver)

FILE = 'sp.csv'
sp = []


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Работа", 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['link']])


driver.get(
    "https://novocherkassk.hh.ru/search/vacancy?salary=30000&schedule=remote&ored_clusters=true&label=not_from_agency&only_with_salary=true&search_period=1&industry=7&education=not_required_or_not_specified&excluded_text=ростелеком%2C+мегафон%2C+мтс%2C+Т-банк%2C+контур&page=0&searchSessionId=10256c92-069c-4ec1-8a32-30162cfe001f&hhtmFrom=vacancy_search_list")

page_fils = ("xpath", "//a[@data-qa='pager-page']")
locator = ("xpath", "//div[text()='Быстрые фильтры']")
profs = ("xpath", "//span[@data-qa='serp-item__title-text']")
hrefs = ("xpath", "//a[@data-qa='serp-item__title']")
pages = driver.find_elements(*page_fils)
locat = driver.find_element(*locator)
profss = driver.find_elements(*profs)
hrefss = driver.find_elements(*hrefs)
time.sleep(3)
j = 0


m =2


action.scroll_to_element(locat).perform()
time.sleep(3)


def pars():
    sp = []
    j = 0
    profss = driver.find_elements(*profs)
    hrefss = driver.find_elements(*hrefs)
    for i in profss:
        print(i.text)
        print(hrefss[j].get_attribute("href"))

        sp.append({'title': i.text,
                   'link': hrefss[j].get_attribute("href")
                   })
        j = j + 1
    return (sp)



end_page = pages[-1].text
print(end_page)
for k in range(int(end_page)-1):
    print("K первый k", k )
    action.scroll_to_element(locat).perform()
    time.sleep(5)
    sp.extend(pars())


    pages = driver.find_elements(*page_fils)
    for page in pages:

        try:
            if int(page.text) == m + k:

                n = pages.index(page)
                print("K", k)
                print("N", n)
                print("M", m)
                print(page.text)

                action.scroll_to_element(locat).perform()
                time.sleep(5)
                # sp.extend(pars())
                wait.until(EC.element_to_be_clickable(pages[n])).click()
                time.sleep(5)
                # m = m+1
        except:
            driver.refresh()




    save_file(sp, FILE)



def scroll_to_element(self, element):  # Скролл к элементу с раскрытием контента под ним
    self.action.scroll_to_element(element).perform()
    self.driver.execute_script("window.scrollTo({top: window.scrollY + 200})")





time.sleep(60)
