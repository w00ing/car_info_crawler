from time import sleep
import csv , string
import pandas as pd
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
#
filename = 'cars_hyundai.csv'
f = open(filename, 'a', encoding='utf8', newline="")
writer = csv.writer(f)



driver = webdriver.Chrome("/Users/awesomeo184/Webdriver/chromedriver")
driver.maximize_window()

url = 'https://www.hyundai.com/kr/ko/e/customer/branch'

driver.get(url)
driver.implicitly_wait(10)

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}

res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

#메뉴바 클릭
# driver.find_element_by_xpath('//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[1]/ul/li[2]/button').click()
# sleep(1)
# #팝업창 닫
# popup_close_button = driver.find_element_by_xpath('//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/div/div[2]/div[1]/button')
# popup_close_button.click()
# sleep(1)



# sleep(2)
# for shop_number in range(1, 11):
#     shop_name_element = driver.find_element_by_xpath(
#         f'//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/ul/li[{shop_number}]/a/b')
#     sleep(0.01)
#     shop_name = shop_name_element.text
#     print(shop_name)
#     shop_list.append(shop_name)
#     sleep(0.5)
# sleep(2)

# TODO: 다음 페이지를 클릭하는건 following-sibling, shop list를 가져오는건 css selector
# TODO: 페이지네이션, 페이지 체인지 안정적으로, shop_list를 가져올 때 마지막 페이지에는 shop이 10개가 아닐 수 있음
# TODO: 첫 페이지에 shop_list가 10개 미만일 수 있음
# 아반떼를 갖고있는 대리점
# def get_shop_info():
#     attrs = True
#     first_page_button = driver.find_element_by_xpath('//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/div/div/ul/li[1]')
#     next_button_elem = driver.find_element_by_xpath(
#         '//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/div/div')
#     next_button = next_button_elem.find_element_by_class_name('btn-next')
#     next_button_attrs = next_button.get_attribute('disabled')
#     while attrs:
#
#         refresh_shop_ul = driver.find_element_by_xpath(
#             '//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/ul')
#         sleep(0.01)
#         refresh_shop_li = refresh_shop_ul.find_elements_by_tag_name('li')
#         refresh_shop_len = len(refresh_shop_li)
#         shop_len = refresh_shop_len
#         print(shop_len)
#         for i in range(1, shop_len+1):
#             print(shop_len)
#             sleep(0.01
#             shop_info_div = driver.find_element_by_xpath(f'//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/ul/li[{i}]')
#
#             shop_name_element = driver.find_element_by_xpath(
#                 f'//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/ul/li[{i}]/a/b')
#             shop_phone_number_element = driver.find_element_by_xpath(f'//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/ul/li[{i}]/p/span')
#             shop_address_element = driver.find_element_by_xpath(f'//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/ul/li[{i}]/span[1]')
#             car_info_element = driver.find_element_by_xpath(f'//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/ul/li[{i}]/span[2]')
#             data_row = [shop_name_element.text, shop_phone_number_element.text, shop_address_element.text, car_info_element.text]
#             print(data_row)
#
#
#         print('forloop tet')
#         if next_button_attrs == True:
#             sleep(0.5)
#             print('operating')
#             first_page_button.click()
#             attrs = False
#         else:
#             print('next button')
#             next_button.click()
#             shop_len = None


#전시차량버튼 클릭
def click_diplayed_car_button():
    displayed_car = driver.find_element_by_xpath('//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[1]/ul/li[2]/button')
    sleep(0.1)
    displayed_car.click()
#차량선택 클릭
def click_model_drop_box():
    model_drop_box = driver.find_element_by_xpath('//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/div/div/div[1]/input')
    sleep(0.1)
    model_drop_box.click()
    sleep(0.1)

#차 모델 클릭
def select_model(i):
    car_model = driver.find_element_by_xpath(f'//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/ul/li[{i}]')
    sleep(0.1)
    car_model.click()
# 크롤링할 대리점 인포 불러오기

#branch > section.content-wrap > div > div > section > section > div.tab.tab--mob > div.tabContents > div.show > section > div.scroll-wrap > ul


def get_shop_info():


    shop_ul_elem = driver.find_element_by_css_selector('section > div.scroll-wrap > ul')
    shop_number_elem = shop_ul_elem.find_elements_by_tag_name('li')
    shop_number = len(shop_number_elem)
    for i in range(1, shop_number+1):
        shop_list_elem = driver.find_element_by_xpath(f'//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/ul/li[{i}]')
        shop_name = shop_list_elem.find_element_by_tag_name('a > b').text
        shop_phone_number = shop_list_elem.find_element_by_tag_name('p > span').text
        shop_address = shop_list_elem.find_elements_by_tag_name('span')[1].text
        shop_region = shop_address.split()[1]
        shop_city = shop_address.split()[2]
        shop_address = shop_address[8::]
        shop_address = shop_address.strip('"')
        car_options = shop_list_elem.find_elements_by_tag_name('span')[2].text
        car_desc = car_options.split()
        if '녹턴' or '스' in car_desc:
            car_color_1 = car_desc.pop(-2)
            car_color_2 = car_desc.pop(-1)
            car_color = car_color_1+car_color_2
        else:
            car_color = car_desc.pop(-1)
        car_desc = " ".join(car_desc)
        shop_data = [shop_name, shop_phone_number, shop_address, shop_region, shop_city, car_desc, car_color, 'hyundai']
        print(shop_data)
        writer.writerow(shop_data)

def page_change():
    pagination_button_list = driver.find_element_by_xpath('//*[@id="branch"]/section[2]/div/div/section/section/div[2]/div[2]/div[2]/section/div[2]/div/div')
    if pagination_button_list.find_element_by_class_name('btn-next'):
        next_button = pagination_button_list.find_element_by_class_name('btn-next')
        next_button_attrs = next_button.get_attribute('disabled')
        if not next_button_attrs:
            next_button.click()

def start_scrapping():

    click_diplayed_car_button()
    click_model_drop_box()
    select_model(19)
    for i in range(76):
        get_shop_info()
        page_change()

start_scrapping()

