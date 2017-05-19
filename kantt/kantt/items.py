# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KanttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title1 = scrapy.Field()
    # title2 = scrapy.Field()
    rate = scrapy.Field()
    url = scrapy.Field()
    pass
