from time import sleep
import csv, string
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


filename = 'chevrolet.csv'
f = open(filename, 'a', encoding='utf8', newline="")
writer = csv.writer(f)

driver = webdriver.Chrome("/Users/awesomeo184/Webdriver/chromedriver")
driver.maximize_window()

url = 'https://www.chevrolet.co.kr/purchase/view-display-car.gm?'

driver.get(url)
driver.implicitly_wait(10)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}

res = requests.get(url, headers=headers)
res.raise_for_status()
html = driver.page_source

soup = BeautifulSoup(res.text, 'lxml')


def page_change():
    next_button = driver.find_elements_by_xpath('//*[@id="FORM_SEARCH"]/div[3]/div/div/span')[-2]
    driver.implicitly_wait(5)
    next_button.click()


def get_info_one_page():
        for i in range(40):
            trs = driver.find_elements_by_xpath('//*[@id="FORM_SEARCH"]/div[3]/table/tbody/tr')
            for tr in trs:
                shop_info = tr.find_elements_by_tag_name('td')[0]
                shop_name = shop_info.find_element_by_tag_name('dl > dt').text
                shop_address = shop_info.find_elements_by_tag_name('dl > dd')[0].text[5:]
                shop_address = shop_address.strip("'., ")
                region = shop_address.split()[0]
                city = shop_address.split()[1]
                shop_phone_number = shop_info.find_elements_by_tag_name('dl > dd')[1].text
                car_name_elem = tr.find_elements_by_tag_name('td')[2]
                car_name = car_name_elem.find_element_by_tag_name('dl > dd').text
                car_color_elem = tr.find_elements_by_tag_name('td')[3]
                car_color = car_color_elem.find_element_by_tag_name('dl > dd').text
                info = [shop_name[:-5], shop_phone_number[7:], shop_address, region, city, car_name, car_color]
                writer.writerow(info)
            page_change()
        get_info_one_page()

get_info_one_page()

driver.close()
