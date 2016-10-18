# -*- coding: utf-8 -*-
import scrapy

from medicrawl.items import NihNlmMedlineItem


class NihNlmMedlineSpider(scrapy.Spider):
    name = "nih-nlm-medline"
    allowed_domains = ["0.0.0.0"]
    start_urls = (
        # should be ftp://ftp.nlm.nih.gov/nlmdata/sample/medline/
        'http://0.0.0.0:8115/',
    )

    def parse_xml_gz(self, response):
        citations = response.xpath('//MedlineCitation')
        for index, citation in enumerate(citations):
            item = NihNlmMedlineItem()
            item['title'] = (citation.xpath('Article/ArticleTitle/text()')
                .extract_first())
            item['abstract'] = (citation.xpath(
                'OtherAbstract/AbstractText/text()').extract_first())
            item['uid'] = '%s-%s' % ('medline',
                citation.xpath('PMID/text()').extract_first())
            item['source'] = 'NihNlmMedlineSpider'
            yield item

    def parse(self, response):
        for url in response.xpath('//a/@href').extract():
            if url.endswith('.xml.gz'):
                abs_url = "%s%s" % (response.url, url)
                yield scrapy.Request(abs_url, callback=self.parse_xml_gz)
