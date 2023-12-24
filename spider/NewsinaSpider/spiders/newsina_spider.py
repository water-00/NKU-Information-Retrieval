# -*- coding: utf-8 -*-

from scrapy import Request
from ..items import *
import random
import json
import re
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException

chrome_options = Options()
chrome_options.add_argument("--headless")

class NewsinaSpider(scrapy.Spider):
    name = 'newsina_spider'
    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'

    def start_requests(self):
        page_total = 100  # 可修改，设置爬取页数
        for page in range(1, page_total + 1):
            lid = "2509"  # 可修改，"2509"代表"全部"类别的新闻
            r = random.random()
            yield Request(self.base_url.format(lid, page, r), callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        data_list = result.get('result').get('data')
        for data in data_list:
            item = NewsinaspiderItem()

            ctime = datetime.fromtimestamp(int(data.get('ctime')))
            ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')

            item['ctime'] = ctime
            item['url'] = data.get('url')
            item['wapurl'] = data.get('wapurl')
            item['title'] = data.get('title')
            item['media_name'] = data.get('media_name')
            item['keywords'] = data.get('keywords')
            yield Request(url=item['url'], callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):
        item = response.meta['item']
        content = ''.join(response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract())
        # 清洗和格式化内容
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = ''.join([x.strip() for x in content])

        item['content'] = content
        item['page_link'] = self.get_page_links(item['url'])

        yield item

    def get_page_links(self, url):
        page_links = []
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(3)
        main_handle = driver.window_handles

        links = driver.find_elements(By.CLASS_NAME, "ty-card-tt")
        for i in range(0, min(len(links), 5)):
            link = links[i]
            try:
                link.click()
            except (ElementClickInterceptedException):
                print("Click intercepted for link:", i)
                continue
            driver.implicitly_wait(1)

        all_handles = driver.window_handles
        for handle in all_handles:
            if handle != main_handle[0]:
                driver.switch_to.window(handle)
                page_links.append(driver.current_url)
                driver.close()

        driver.switch_to.window(main_handle[0])
        driver.quit()

        return page_links
