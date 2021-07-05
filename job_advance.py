from selenium import webdriver
from selenium.webdriver import Chrome

import csv
import sys
import time
import re

# 取得したデータの参照のため
import json


def main():
    args = sys.argv
    dir_name = None
    try:
        dir_name = args[1]
    except IndexError:
        pass

    replace_table = str.maketrans({
        '\u3000': '',
        ' ': '',
        '\n': ''
    })

    item_labels = [
        'company_name',
        'location',
        'pref',
        'receptionist',
        'type_of_work',
        'employment_status',
        'phone_number',
        'mail_address',
        'job_advance_url'
    ]

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    page_urls = []
    start_url = 'https://jobadvance.jp/category/%e5%85%a8%e5%9b%bd/'
    page_urls.append(start_url)

    with open('job_article.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=item_labels)
        writer.writeheader()

    for page_url in page_urls:
        driver.get(page_url)
        next_page = driver.find_element_by_css_selector('li.next > a.next.page-numbers').get_attribute('href')
        if next_page is not None:
            page_urls.append(next_page)

        article_urls = []
        jobs = driver.find_elements_by_css_selector('ol#post_list2 li.article')
        for job in jobs:
            article_url = job.find_element_by_css_selector('a').get_attribute('href')
            article_urls.append(article_url)
            time.sleep(3)

        for article_url_list in article_urls:
            driver.get(article_url_list)

            item = {}
            job_advance_url = article_url_list
            item['job_advance_url'] = job_advance_url
            time.sleep(3)
            table_tr_selectors = driver.find_elements_by_css_selector('table.wp-block-table > tbody > tr')
            pref = None
            for table_tr_selector in table_tr_selectors:
                content_name = table_tr_selector.find_element_by_css_selector('td:nth-of-type(1)').text
                content_data = table_tr_selector.find_element_by_css_selector('td:nth-of-type(2)').text.translate(replace_table)
                if "会社名" in content_name:
                    company_name = content_data
                    item['company_name'] = company_name
                if "所在地" in content_name:
                    location = content_data
                    item['location'] = location
                    pref = re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県', location).group()
                    item['pref'] = pref
                if "受付担当者" in content_name:
                    receptionist = content_data.replace('採用担当/', '')
                    item['receptionist'] = receptionist
                if "職種" in content_name:
                    type_of_work = content_data
                    item['type_of_work'] = type_of_work
                if "雇用形態" in content_name:
                    employment_status = content_data
                    item['employment_status'] = employment_status

            contact_selectors = driver.find_elements_by_css_selector('div.post_content.clearfix')
            for contact_selector in contact_selectors:
                if len(contact_selector.find_elements_by_css_selector('p:nth-of-type(2)')) > 0:
                    phone_number_text_content = contact_selector.find_element_by_css_selector('p:nth-of-type(2)').text
                    phone_number_a_content = contact_selector.find_element_by_css_selector('p a').text
                    if "電話で応募する：" in phone_number_text_content:
                        phone_number = phone_number_a_content
                        item['phone_number'] = phone_number
                if len(contact_selector.find_elements_by_css_selector('p:nth-of-type(3) a')) > 0:
                    mail_address_text_content = contact_selector.find_element_by_css_selector('p:nth-of-type(3)').text
                    mail_address_a_content = contact_selector.find_element_by_css_selector('p:nth-of-type(3) a').text
                    if "メールで応募する：" in mail_address_text_content:
                        mail_address = mail_address_a_content
                        item['mail_address'] = mail_address

            # 取得したデータの参照　不要の場合はコメントアウトして下さい。
            if dir_name == pref or dir_name is None:
                item_elem = json.dumps(item, ensure_ascii=False)
                print(item_elem.replace(',', ',\n'))

                with open('job_article.csv', 'a', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=item_labels)
                    writer.writerow(item)
            driver.back()
    driver.close()


if __name__ == "__main__":
    main()