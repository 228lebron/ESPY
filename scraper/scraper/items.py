# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    quantity = scrapy.Field()
    days_until_shipment = scrapy.Field()
    special_mark_hit = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()

class PromItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    quantity = scrapy.Field()
    is_new = scrapy.Field()
    is_sale = scrapy.Field()
    date = scrapy.Field()
