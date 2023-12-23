# -*- coding: utf-8 -*-

from scrapy import Request
from ..items import *
import random
import json
import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import  ElementClickInterceptedException

chrome_options = Options()
chrome_options.add_argument("--headless")

class PageRankSpider(scrapy.Spider):
    name = 'pagerank_spider'

    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'

    def start_requests(self):
        page_total = 1
        for page in range(1, page_total+1):
            lid = "2509"  # "全部" 类别的新闻
            r = random.random()
            yield Request(self.base_url.format(lid, page, r), callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        data_list = result.get('result').get('data')
        
        for data in data_list:
            item = PagerankItem()
            item['url'] = data.get('url')
            item['wapurl'] = data.get('wapurl')
            yield Request(url=item['url'], callback=self.get_related_link, meta={'item': item})

    def get_related_link(self, response):
        item = response.meta['item']
        item['page_link'] = []
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(item['url'])
        print("item['url']: ", item['url'])
        
        # Scroll down to the bottom of the page to ensure all elements are loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(5)
        main_handle = driver.window_handles
        
        links = driver.find_elements(By.CLASS_NAME, "ty-card-tt")
        for i in range(0, 10):
            # Use JavaScript to click the link
            link = links[i]
            try:
                link.click()
            except (ElementClickInterceptedException):
                print(1)
            driver.implicitly_wait(1)
            

        # 获取所有窗口句柄
        all_handles = driver.window_handles
        print(all_handles)
        
        # 遍历窗口句柄
        for handle in all_handles:
            driver.switch_to.window(handle)
            if main_handle[0] != handle:
                item['page_link'].append(driver.current_url)
                print("page_link: ", driver.current_url)

        print(item['page_link'])
        driver.quit()
        time.sleep(1)
        yield item
