# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import logging
import sqlite3


class SQLitePipeline(object):
    def __init__(self):
        self.conn = sqlite3.connect("slikdeals.sqlite")
        self.cur = self.conn.cursor()
        self.crate_table()

    def crate_table(self):
        self.cur.executescript("""
            DROP TABLE IF EXISTS Tech;
            CREATE TABLE Tech (
            sl INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            product_name TEXT,
            product_price TEXT,
            old_price TEXT,
            product_rating TEXT,
            no_of_ratings TEXT,
            product_link TEXT );
            """)
        self.conn.commit()

    def process_item(self, item, spider):
        a = item.get("product_name")
        b = item.get("product_price")
        c = item.get("old_price")
        d = item.get("product_rating")
        e = item.get("no_of_ratings")
        f = item.get("product_link")
        self.cur.execute("""
            INSERT INTO Tech (product_name, product_price, old_price, product_rating, no_of_ratings, product_link) 
            VALUES (?,?,?,?,?,?)
        """, (a, b, c, d, e, f))
        self.conn.commit()
        return item
