# -*- coding: utf-8 -*-

from scrapy import Request
from ..items import *
import random
import json
import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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
        
        # Scroll down to the bottom of the page to ensure all elements are loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            # Wait for the dynamically loaded elements to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, ".ty-card-tt"))
            )
        except TimeoutException:
            print("Timeout waiting for elements to load.")
            driver.quit()
            return
        
        # links = driver.find_elements(By.CSS_SELECTOR, ".ty-card.ty-card-type1.clearfix")
        links = driver.find_elements(By.CLASS_NAME, "ty-card-tt")
        for link in links:
            try:
                main_window = driver.current_window_handle
                link.click()  # This might open a new window, depending on the page behavior
                # Wait for the new window to open
                WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                new_window = [window for window in driver.window_handles if window != main_window][0]
                driver.switch_to.window(new_window)
                l = driver.current_url
                item['page_link'].append(l)
                print("--------", l, "--------\n\n\n")
                
                with open('page_links.txt', 'a', encoding='utf-8') as f:
                    f.write(l + '\n')        
                
                time.sleep(30)
                driver.close()  # Close the new window
                driver.switch_to.window(main_window)  # Switch back to the main window
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Error clicking on link or handling new window: {e}")
        
        driver.quit()
        yield item
