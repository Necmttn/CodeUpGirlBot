import scrapy
import json

# osman

with open('users.json') as data_file:
    data = json.load(data_file)

def genUserUrl(userList):
    userUrl = []
    for user in userList:
        userUrl.append(''.join(['https://www.freecodecamp.com/', user]))
    return userUrl

userUrls = genUserUrl(data["users"])

class BlogSpider(scrapy.Spider):
    name = 'FreeCodeCampScrapper'
    start_urls = userUrls

    def parse(self, response):
        name =  response.xpath('//h1[@class="flat-top wrappable"]/text()').extract_first()
        bio = response.xpath('//p[@class="flat-top bio"]/text()').extract_first()
        score =  response.xpath('//h1[@class="flat-top text-primary"]/text()').extract_first()
        yield { 'name': name, 'bio': bio, 'score': score }
