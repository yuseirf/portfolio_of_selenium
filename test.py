import csv
from selenium import webdriver
from selenium.webdriver import Chrome
import pdb

replace_table = str.maketrans({
    '\u3000': '',
    ' ': ''
})

item_labels = [
    'company_name',
    'location',
    'receptionist',
    'type_of_work',
    'employment_status',
    'phone_number',
    'mail_address'
]

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://jobadvance.jp/category/%e5%85%a8%e5%9b%bd/')

for job in driver.find_elements_by_css_selector('ol#post_list2 li.article'):
    a_article = job.find_element_by_css_selector('a')
    a_article.click()

    item = {}
    table_tr_selectors = driver.find_elements_by_css_selector('table.wp-block-table > tbody > tr')
    for table_tr_selector in table_tr_selectors:
        content_name = table_tr_selector.find_element_by_css_selector('td:nth-of-type(1)').text
        content_data = table_tr_selector.find_element_by_css_selector('td:nth-of-type(2)').text.translate(replace_table)
        if "会社名" in content_name:
            item['company_name'] = content_data
            company_name = item['company_name']
        if "所在地" in content_name:
            item['location'] = content_data
            location = item['location']
        if "受付担当者" in content_name:
            item['receptionist'] = content_data.replace('採用担当 / ', '')
            receptionist = item['receptionist']
        if "職種" in content_name:
            item['type_of_work'] = content_data
            type_of_work = item['type_of_work']
        if "雇用形態" in content_name:
            item['employment_status'] = content_data

    contact_selectors = driver.find_elements_by_css_selector('div.post_content.clearfix')
    for contact_selector in contact_selectors:
        phone_number_text_content = contact_selector.find_element_by_css_selector('p:nth-of-type(2)').text
        phone_number_a_content = contact_selector.find_element_by_css_selector('p > a').text
        if "電話で応募する：" in phone_number_text_content:
            item['phone_number'] = phone_number_a_content
            phone_number = item['phone_number']

        mail_address_text_content = contact_selector.find_element_by_css_selector('p:nth-of-type(3)').text
        mail_address_a_content = contact_selector.find_element_by_css_selector('p:nth-of-type(3) > a').text
        if mail_address_text_content is not None and "メールで応募する：" in mail_address_text_content:
            item['mail_address'] = mail_address_a_content
            mail_address = item['mail_address']
    # 取得したitemをcsvファイルに書き込み
    with open('job_article.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=item_labels)
        writer.writeheader()
        writer.writerow(item)

    driver.back()

driver.close()