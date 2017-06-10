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
            if item['name']:
                utils.insert_db('INSERT INTO results(name,bio,score) \
                                VALUES(?,?,?)',
                                (
                                item['name'],
                                item['bio'],
                                self.sanitize_score(item.get('score'))))
        except Exception as e:
            logger.exception(e)
            print('Failed to insert item: {}'.format(item['name']))
        return item

    def open_spider(self, spider):
        self.refresh_table(self.filename)

    def close_spider(self, spider):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def sanitize_score(self, string=''):
        try:
            return int(string.strip(' []'))
        except:
            return 0

    def refresh_table(self, filename):
        utils.insert_db('DROP TABLE result')
        self.conn.execute('create table if not exists results \
                     ( \
                     id integer primary key, \
                     name text unique, \
                     bio text, \
                     score integer)')
        self.conn.commit()

