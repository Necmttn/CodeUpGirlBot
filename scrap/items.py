import scrapy


class ScrapItem(scrapy.Item):

    name = scrapy.Field()

    bio = scrapy.Field()

    score = scrapy.Field()

    def __str__(self):
        return self['name']
