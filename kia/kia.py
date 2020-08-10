# -*- coding: utf-8 -*-
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if 1 == len(siblings)
            else "%s[%d]"
            % (child.name, next(i for i, s in enumerate(siblings, 1) if s is child))
        )
        child = parent
    components.reverse()
    return "/%s" % "/".join(components)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

driver = webdriver.Chrome("/Users/koooo/Webdriver/chromedriver")


driver.implicitly_wait(3)

driver.get("https://www.kia.com/kr/experience-center/display-car/default.html")

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

# Select model


def get_models():

    models_ul = driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/div/div[2]/div/div/div/span[1]/span/div/ul'
    )

    models = models_ul.find_elements_by_tag_name("li")[1:]

    return models


def get_regions():

    regions_ul = driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/div/div[2]/div/div/div/span[4]/span/div/ul'
    )

    regions = regions_ul.find_elements_by_tag_name("li")[1:]
    return regions


def get_cities():

    cities_ul = driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/div/div[2]/div/div/div/span[6]/span/div/ul'
    )

    cities = cities_ul.find_elements_by_tag_name("li")[1:]
    return cities


models_options = driver.find_element_by_xpath(
    '//*[@id="content"]/div/div[2]/div/div[2]/div/div/div/span[1]/span/div/div[2]'
)
# models_options.click()
# models = get_models()


def get_shop_info(soup):

    shops = []

    # shop_container = soup.find_all()
    shop_list = soup.select("li.sectionInner.ng-scope")
    try:
        for shop in shop_list:
            # print(shop)
            shop_name = shop.select(".branch.ng-binding")[0].text
            print(shop_name)
            shop_phone_number = shop.select(".tel.ng-binding")[0].text
            print(shop_phone_number)

            address_btn = shop.select("div.demonBtn > div:nth-child(2) > a")[0]
            xpath = xpath_soup(address_btn)
            driver.find_element_by_xpath(xpath).click()

            shop_address = soup.select(
                "#locationLayer > div > div > div.inforBox > ul > li:nth-child(2)"
            )[0].text[5:]
            print(shop_address)
            address_city = shop_address.split()[0]
            address_region = shop_address.split()[1]
            car_model_full = shop.select(
                "div.demonsBox > ul.carInfor > li:nth-child(1) > span.output.ng-binding"
            )[0].text
            # car_model = soup.select(
            # "#content > div > div.content_detail.search_inventory.section > div > div.con_search > div > div > div > span:nth-child(1) > span > div > div.form_spr.selected-headline > span"
            # )[0].text
            # car_model = driver.find_element_by_xpath(
            # '//*[@id="content"]/div/div[2]/div/div[2]/div/div/div/span[1]/span/div/div[2]/span'
            # ).text
            # car_model_trim = car_model_full.replace(car_model, "")
            # print(car_model)
            car_color = shop.select("li:nth-child(2) > span.output.ng-binding")[
                0
            ].text.strip()

            print(car_color)
            driver.find_element_by_xpath('//*[@id="locationLayer"]/a').click()

            shop_info = {
                "shop_name": shop_name,
                "shop_phone_number": shop_phone_number,
                "shop_address": shop_address,
                "address_city": address_city,
                "address_region": address_region,
                "car_model_full": car_model_full,
                # "car_model": car_model,
                # "car_model_trip": car_model_trim,
                "car_color": car_color,
            }
            shops.append(shop_info)
        return shops
    except:
        return 0


data = []

df = pd.DataFrame()


def get_last_page():
    driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/div/div[4]/div/a[9]'
    ).click()
    last_page = 1
    for i in reversed(range(3, 8)):
        try:
            last_page = int(
                driver.find_element_by_xpath(
                    f'//*[@id="content"]/div/div[2]/div/div[4]/div/a[{i}]'
                ).text
            )
        except:
            continue

    driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/div/div[4]/div/a[1]'
    ).click()
    return last_page


i = 1
current_page = 401
click_count = 0
while click_count < 100:
    driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/div/div[4]/div/a[8]'
    ).click()
    click_count += 1


while current_page < 638:
    for index in range(4, 9):
        try:
            loop_html = driver.page_source
            loop_soup = BeautifulSoup(loop_html, "html.parser")
            shops = get_shop_info(loop_soup)
            datumframe = pd.DataFrame(shops)
            df = df.append(datumframe)
            # data.append(shops)
            driver.find_element_by_xpath(
                f'//*[@id="content"]/div/div[2]/div/div[4]/div/a[{index}]'
            ).click()
            # time.sleep(1)
            current_page += 1
            print(current_page)
        except:
            current_page += 1
            continue

print(data)
# regions_options.click()


driver.quit()

# for index, datum in enumerate(data):
#     datumframe = pd.DataFrame(datum)
#     # datumframe.to_excel(f"test{index}.xlsx", index=None)
#     df = df.append(datumframe)


df.to_excel("kia_data_6.xlsx", index=None)

