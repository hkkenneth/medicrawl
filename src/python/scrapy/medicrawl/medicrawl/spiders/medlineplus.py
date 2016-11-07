# -*- coding: utf-8 -*-
import scrapy

from medicrawl.items import MedlinePlusItem


class MedlineplusSpider(scrapy.spiders.XMLFeedSpider):
    name = "medlineplus"
    allowed_domains = ["medlineplus.gov"]
    start_urls = (
        # should be https://medlineplus.gov/xml/mplus_topics_2016-10-15.xml
        # or other more updated links from https://medlineplus.gov/xml.html
        #'http://0.0.0.0:8114/1000.xml',
        'http://0.0.0.0:8114/mplus_topics_2016-10-15.xml',
    )
    itertag = 'health-topic'

    def parse_node(self, response, node):
        item = MedlinePlusItem()
        # https://github.com/knockrentals/scrapy-elasticsearch/issues/41
        item['uid'] = [('%s-%s' % ('medline-plus',
                                  node.xpath('@id').extract_first()))]
        item['title'] = node.xpath('@title').extract_first()
        item['summary'] = node.xpath('full-summary/text()').extract_first()
        item['source'] = 'MedlineplusSpider'
        return item
