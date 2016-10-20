# -*- coding: utf-8 -*-
import scrapy

from medicrawl.items import NHSChoicesItem


class NHSChoicesSpider(scrapy.Spider):
    name = "nhs-choices"
    allowed_domains = ["www.nhs.uk"]
    start_urls = (
        'http://www.nhs.uk/Conditions/Pages/hub.aspx',
    )

    def parse_topic_page(self, response):
        text = response.xpath("//div[contains(@class, 'main-content')]"
                              "/div[@id='webZoneLeft']/"
                              "preceding-sibling::node()"
                              ).xpath("descendant-or-self::*/text()").extract()
        item = NHSChoicesItem()
        item['uid'] = '%s-%s' % ('nhs-choice', response.url.split('/')[4])
        item['title'] = response.css("div.healthaz-header h1::text"
                                     ).extract_first()
        item['content'] = ' '.join(text)
        item['source'] = 'NHSChoicesSpider'
        return item

    def parse_index_list(self, response):
        for url in response.css("div.index-section a").xpath("@href").extract():
            abs_url = 'http://www.nhs.uk' + url
            yield scrapy.Request(abs_url, callback=self.parse_topic_page)

    def parse(self, response):
        for url in response.css("div#haz-mod1 li a").xpath("@href").extract():
            abs_url = 'http://www.nhs.uk/Conditions/Pages/' + url
            yield scrapy.Request(abs_url, callback=self.parse_index_list)
