# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MedicrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NihNlmMedlineItem(scrapy.Item):
    source = scrapy.Field()
    uid = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    pass
