# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3

class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class SqliteCompelPipeline:

    def __init__(self):
        print('Текущий юзер:', os.getlogin())
        print('Текущая рабочая директория:', os.getcwd())
        ## Create/Connect to database
        if not os.path.isfile('/home/ESPY/scraper/products.db'):
            self.con = sqlite3.connect('/home/ESPY/scraper/products.db')
        else:
            self.con = sqlite3.connect('/home/ESPY/scraper/products.db')

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS compel_data(
            name TEXT,
            brand TEXT,
            price REAL,
            quantity INT,
            days_until_shipment INT,
            url TEXT,
            date DATE
        )
        """)

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute("""
            INSERT INTO compel_data (name, brand, price, quantity, days_until_shipment, url, date) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
                         (
                             item['name'],
                             item['brand'],
                             item['price'],
                             item['quantity'],
                             item['days_until_shipment'],
                             item['url'],
                             item['date'],
                         ))

        ## Execute insert of data into database
        self.con.commit()
        return item

