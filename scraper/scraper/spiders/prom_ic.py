import scrapy
from scraper.items import PromItem
import re
import datetime


class PromIcSpider(scrapy.Spider):
    name = 'prom_ic'
    allowed_domains = ['www.promelec.ru']
    start_urls = ['https://www.promelec.ru/catalog/1/2/',
                  'https://www.promelec.ru/catalog/1/10/',
                  'https://www.promelec.ru/catalog/1/11/',
                  'https://www.promelec.ru/catalog/1/18/',
                  'https://www.promelec.ru/catalog/1/19/',
                  'https://www.promelec.ru/catalog/1/20/',
                  'https://www.promelec.ru/catalog/1/12/',
                  'https://www.promelec.ru/catalog/1/13/',
                  'https://www.promelec.ru/catalog/1/14/',
                  'https://www.promelec.ru/catalog/1/21/',
                  'https://www.promelec.ru/catalog/1/26/',
                  'https://www.promelec.ru/catalog/1/24/',
                  'https://www.promelec.ru/catalog/1/15/',
                  'https://www.promelec.ru/catalog/1/16/',
                  'https://www.promelec.ru/catalog/1/17/',
                  'https://www.promelec.ru/catalog/1/2380/',
                  'https://www.promelec.ru/catalog/1/2427/',
                  ]

    def start_requests(self):
        cookies = {'pageSize': '60'}
        for url in self.start_urls:
            yield scrapy.Request(f'{url}?instock=1&smartFilter=0', cookies=cookies)

    def parse(self, response):
        table_list_items = response.css('.table-list__item')
        category = response.xpath('//h1/text()').get()

        #for item in table_list_items:
        #    title = item.css('a.product-preview__title::attr(title)').get()
        #    brand = item.css('span.product-preview__code i a::text').get()
        #    quantity = item.css('span.table-list__counter::text').extract_first().replace(' ', '')
        #    price_str = item.css('span.table-list__price::text').get()
        #    price = price_str.replace('от ', '').replace(',', '.').strip()
        #    is_new = item.css('span.pr-badge.badge-new::text').get()
        #    is_sale = item.css('span.pr-badge.badge-sale::text').get()
#
        #    product_item = PromItem()
#
        #    product_item['category'] = category
        #    product_item['name'] = title
        #    product_item['brand'] = brand
        #    product_item['price'] = price
        #    product_item['quantity'] = quantity
        #    product_item['is_new'] = is_new
        #    product_item['is_sale'] = is_sale
        #    product_item['date'] = datetime.date.today()
#
        #    yield product_item

        product_items = [PromItem(
            category=category,
            name=item.css('a.product-preview__title::attr(title)').get(),
            brand=item.css('span.product-preview__code i a::text').get(),
            price=item.css('span.table-list__price::text').get().replace('от ', '').replace(',', '.').strip(),
            quantity=item.css('span.table-list__counter::text').extract_first().replace(' ', ''),
            is_new=item.css('span.pr-badge.badge-new::text').get(),
            is_sale=item.css('span.pr-badge.badge-sale::text').get(),
            date=datetime.date.today()
        ) for item in table_list_items]

        yield product_items


        next_page = response.css('.paging-next__link::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
