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
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument("--headless")

class NewsinaSpider(scrapy.Spider):
    name = 'newsina_spider'
    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'

    def __init__(self, *args, **kwargs):
        super(NewsinaSpider, self).__init__(*args, **kwargs)
        # MongoDB 连接设置
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Newsina']  # 你的数据库名
        self.collection = self.db['newsina']  # 你的集合名


    def start_requests(self):
        page_total = 10  # 可修改，设置爬取页数
        for page in range(1, page_total + 1):
            lids = [
                "2511"#, "2669", "2512", "2513", "2514", "2515", "2516", "2517", "2518", "2968", "2970", "2972", "2974"
            ]  # 所有类别的ID
            
            #     "2509": "全部",
            #     "2510": "国内",
            #     "2511": "国际",
            #     "2669": "社会",
            #     "2512": "体育",
            #     "2513": "娱乐",
            #     "2514": "军事",
            #     "2515": "科技",
            #     "2516": "财经",
            #     "2517": "股市",
            #     "2518": "美股",
            #     "2968": "国内_国际",
            #     "2970": "国内_社会",
            #     "2972": "国际_社会",
            #     "2974": "国内国际社会"

            for lid in lids:
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

            # 查询 MongoDB 确认 URL 是否已经存在
            if self.collection.find_one({'url': item['url']}):
                print(f"URL已存在，跳过：{item['url']}")
                continue  # 如果存在，则跳过该项

            # 如果 URL 不存在，则继续进行后续操作
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

    def closed(self, reason):
        self.client.close()  # 爬虫关闭时关闭 MongoDB 连接