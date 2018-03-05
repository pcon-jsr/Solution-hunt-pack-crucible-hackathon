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
        self.queries = query.split(",")
        self.points = {}
        point  = len(self.queries)
        for q in self.queries:
            self.points[q] = point
            point = point - 1
        for i in range(len(self.queries)):
            for j in range(i+1,len(self.queries)):
                self.start_urls.append('http://www.google.co.in/search?q=%s' % self.queries[i]+'  '+self.queries[j])
        #self.start_urls = ['http://www.google.co.in/search?q=%s' % query]

    def parse(self, response):
        urls = response.css("h3.r a::attr(href)").extract()
        titles = response.xpath(".//h3[@class='r']").xpath("string()").extract()
        descriptions = response.xpath(".//span[@class='st']").xpath("string()").extract()
        for url,desc,title in zip(urls, descriptions,titles):
            parsed_url = url
            desc = desc.replace("\n", " ")
            tag_str = urlparse(response.url).query
            tag_str = tag_str.split("&")
            tag_str = tag_str[0]
            tag_str = tag_str[2:]
            tag_str = tag_str.replace("%20"," ")
            tags = tag_str.split("  ")
            point = self.points[tags[0]] * self.points[tags[1]]
            typ = "Webpage"
            if("pdf" in url):
                typ = "Document"
            elif("youtube" in url):
                typ = "Youtube video"
            elif("wikipedia" in url):
                typ = "Wiki"
            yield {'search url' : response.url, 'url' : parsed_url, 'description' : desc, 'tags' : tags, 'title' : title, 'type' : typ, 'score' : point}
