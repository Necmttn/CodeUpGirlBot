# -*- coding: utf-8 -*-
import scrapy

from scrap import utils


class FccCrawlSpider(scrapy.Spider):
    name = 'fcc_crawl'
    allowed_domains = ['freecodecamp.com']

    start_urls = ['http://freecodecamp.com/{}'.format(u)
                  for u in utils.query_db(
                      'SELECT username \
                       FROM students \
                       WHERE is_active=1')]

    def parse(self, response):
        name =  response.xpath(
            '//h1[@class="flat-top wrappable"]/text()'
            ).extract_first()

        bio = response.xpath(
            '//p[@class="flat-top bio"]/text()'
            ).extract_first()

        score =  response.xpath(
            '//h1[@class="flat-top text-primary"]/text()'
            ).extract_first()

        yield { 'name': name, 'bio': bio, 'score': score }
