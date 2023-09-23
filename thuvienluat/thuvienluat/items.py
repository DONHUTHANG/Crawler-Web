# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ThuvienluatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def serialize_question(value):
    return f'{str(value)}'

class DataItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    h2_title= scrapy.Field()
    paragraph = scrapy.Field()
