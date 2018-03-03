# -*- coding: utf-8 -*-
import scrapy
from urlparse import urljoin, urlparse, parse_qsl
import re

def _parse_url(href):
    queries = dict(parse_qsl(urlparse(href).query))
    return queries.get('q', '')



class Spider2Spider(scrapy.Spider):
    name = 'spider2'
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.ValidatePipeline': 300,
            }
        }

    def __init__(self, query=None, *args, **kwargs):
        super(Spider2Spider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.google.co.in/search?q=%s' % query]

    def parse(self, response):
        urls = response.css("div.g h3.r a::attr(href)").extract()
        descriptions = response.xpath(".//span[@class='st']").xpath("string()").extract()
        for url,desc in zip(urls, descriptions):
            parsed_url = _parse_url(url)
            desc = desc.replace("\n", " ")
            yield {'orignal url' : url, 'url' : parsed_url, 'description' : desc}
