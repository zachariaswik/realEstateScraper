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
        INSERT OR REPLACE INTO listings (listingName, location, price, rooms, bathrooms, sizeConstr, sizeUtil, sizeSolar, floor, type, exterior, interior, age, state, reference, communityCost, description, Erating, CO2rating, Econsumption, CO2emission, last_update)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('listingName'),
            item.get('location'),
            item.get('price'),
            item.get('rooms'),
            item.get('bathrooms'),
            item.get('sizeConstr'),
            item.get('sizeUtil'),
            item.get('sizeSolar'),
            item.get('floor'),
            item.get('type'),
            item.get('exterior'),
            item.get('interior'),
            item.get('age'),
            item.get('state'),
            item.get('reference'),
            item.get('communityCost'),
            item.get('description'),
            item.get('Erating'),
            item.get('CO2rating'),
            item.get('Econsumption'),
            item.get('CO2emission'),
            item.get('last_update')
        ))
        self.conn.commit()
        return item
