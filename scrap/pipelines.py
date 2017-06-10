import sqlite3
import logging

from os import path

from scrapy import signals
from scrap import utils


logger = logging.getLogger('pipeline')


class SQLiteStorePipeline(object):
    filename = '/app/db/database.db'

    def __init__(self):
        self.conn = utils.get_connection_to_db(self.filename)

    def process_item(self, item, domain):
        try:
            utils.query_db('insert into results(name,bio,score) \
                              values(?,?,?)',
                              (
                              item['name'],
                              item['bio'],
                              int(item['score'].strip(' []'))))
        except Exception as e:
            logger.exception(e)
            print('Failed to insert item: {}'.format(item['name']))
        return item

    def open_spider(self, spider):
        self.create_table(self.filename)

    def close_spider(self, spider):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        self.conn.execute('create table if not exists results \
                     ( \
                     id integer primary key, \
                     name text, \
                     bio text, \
                     score integer)')
        self.conn.commit()

