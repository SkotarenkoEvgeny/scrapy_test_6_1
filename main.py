import os
import csv
import time

from selenium import webdriver

URL = 'https://www.zooplus.de/tierarzt/results?animal_99=true#'
FILENAME = "result.csv"
page_count = int(input('Set a count of pages: '))
data_set = []

browser = webdriver.Chrome(executable_path=os.path.join('..\Include\chromedriver\chromedriver.exe'))

try:
    browser.get(URL)
    time.sleep(2)
    set_cookie_rule = browser.find_element_by_id('onetrust-reject-all-handler')
    if set_cookie_rule:
        set_cookie_rule.click()
    start_page = browser.find_element_by_xpath('//nav/ul/li[last()]/a')
    start_page.click()

    for i in range(page_count):
        work_time = []
        # name_place lit
        name_feature = [i.text for i in
                        browser.find_elements_by_xpath('//article/a/div[@class="result-intro__details"]/header/h1')]
        # addres list
        addres = [i.text for i in browser.find_elements_by_xpath('//p[@class="result-intro__address"]')]
        # rating
        rating = [i.text for i in browser.find_elements_by_xpath('//span[@class="result-intro__rating__note"]')]

        raw_place_time = [i.text.split('\n') for i in
                          browser.find_elements_by_xpath('//div[@class="result-intro__subheader"]')]
        for count, elem in enumerate(raw_place_time):
            if len(elem) == 1:
                raw_work_time = elem[0]
            else:
                name_feature[count] += f'\n{elem[0]}'
                raw_work_time = elem[1]

            raw_dict = {'name_feature': name_feature[count],
                        'work_time': raw_work_time,
                        'rating': rating[count],
                        'addres': addres[count]}
            # check duplicates
            if raw_dict not in data_set:
                data_set.append(raw_dict)

        time.sleep(2)
        next_page = browser.find_element_by_xpath('//nav/ul/li[last()]/a')
        print(next_page.get_attribute('href'))
        next_page.click()

except Exception as ex:
    print(f'exception {ex}')

finally:
    browser.close()
    browser.quit()

with open(FILENAME, "w", newline='', encoding='UTF-8') as file:
    columns = ['name_feature', 'work_time', 'rating', 'addres']
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(data_set)
