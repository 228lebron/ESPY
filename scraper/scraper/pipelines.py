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

        self.con = sqlite3.connect('/home/ESPY/scraper/products.db')
        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS compel_data(
            category TEXT,
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
        ## Check to see if text is already in database
        self.cur.execute("""SELECT * FROM compel_data WHERE url=? AND date=?""", (item['url'], item['date']))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            self.cur.execute("""
                            UPDATE compel_data SET 
                                category = ?,
                                name = ?,
                                brand = ?,
                                price = ?,
                                quantity = ?,
                                days_until_shipment = ?
                            WHERE url = ? AND date = ?
                        """,
                             (
                                 item['category'],
                                 item['name'],
                                 item['brand'],
                                 item['price'],
                                 item['quantity'],
                                 item['days_until_shipment'],
                                 item['url'],
                                 item['date']
                             ))
            self.con.commit()
            spider.logger.warn("Item updated in database: %s" % item['url'])

        ## If text isn't in the DB, insert data
        else:
            ## Define insert statement
            self.cur.execute("""
                INSERT INTO compel_data (category, name, brand, price, quantity, days_until_shipment, url, date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                             (
                                 item['category'],
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

