# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class PisosscraperPipeline:
    def process_item(self, item, spider):
        return item





class SQLitePipeline:

    def open_spider(self, spider):
        self.conn = sqlite3.connect('pisos_listings.db')
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
        INSERT OR IGNORE INTO listings (listingName, location, price, rooms, bathrooms, size, floor, type)
        VALUES (?,?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('listingName'),
            item.get('location'),
            item.get('price'),
            item.get('rooms'),
            item.get('bathrooms'),
            item.get('size'),
            item.get('floor'),
            item.get('type')
        ))
        self.conn.commit()
        return item