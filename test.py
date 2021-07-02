from selenium import webdriver
from selenium.webdriver import Chrome
import pdb

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://jobadvance.jp/category/%e5%85%a8%e5%9b%bd/')

for job in driver.find_elements_by_css_selector('ol#post_list2 li.article'):
    a_article = job.find_element_by_css_selector('a')
    a_article.click()
    item = {}
    table_tr_selectors = driver.find_elements_by_css_selector('table.wp-block-table > tbody > tr')
    for table_tr_selector in table_tr_selectors:
        content_information = table_tr_selector.find_element_by_css_selector('td:nth-of-type(1)').text
        content_data = table_tr_selector.find_element_by_css_selector('td:nth-of-type(2').text

        if "会社名" in content_information:
            item['company_name'] = content_data
            company_name = item['company_name']
        if "所在地" in content_information:
            item['location'] = content_data.replace(' ', '')
            location = item['location']
        print(item)

driver.close()