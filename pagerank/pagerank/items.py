# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PagerankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'pagerank'
    url = scrapy.Field()
    wapurl = scrapy.Field()
    page_link = scrapy.Field()