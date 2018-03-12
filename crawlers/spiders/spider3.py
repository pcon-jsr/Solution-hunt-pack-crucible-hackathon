# -*- coding: utf-8 -*-
import scrapy
from urlparse import urljoin, urlparse, parse_qsl
import re
from math import sqrt

def _parse_url(href):
    queries = dict(parse_qsl(urlparse(href).query))
    return queries.get('q', '')



class Spider3Spider(scrapy.Spider):
    name = 'spider3'
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.ValidatePipeline': 300,
            }
        }

    def __init__(self, query=None, *args, **kwargs):
        super(Spider3Spider, self).__init__(*args, **kwargs)
        self.queries = query.split(",")
        self.points = {}
        self.n_queries = len(self.queries)
        point  = len(self.queries)
        for q in self.queries:
            self.points[q] = point
            point = point - 1
        if(self.n_queries>=3):
            self.start_urls.append('http://www.bing.com/search?cc=in&q=%s' % self.queries[0]+'  '+self.queries[1]+'  '+self.queries[2])
        for i in range(len(self.queries)):
            for j in range(i+1,len(self.queries)):
                self.start_urls.append('http://www.bing.com/search?cc=in&q=%s' % self.queries[i]+'  '+self.queries[j])
        #self.start_urls = ['http://www.google.co.in/search?q=%s' % query]

    def parse(self, response):
        urls = response.css("li.b_algo h2 a::attr(href)").extract()
        titles = response.xpath(".//li[@class='b_algo']//h2//a").xpath("string()").extract()
        descriptions = response.xpath(".//div[@class='b_caption']//p").xpath("string()").extract()
        for url,desc,title in zip(urls, descriptions,titles):
            parsed_url = url
            desc = desc.replace("\n", " ")
            tag_str = urlparse(response.url).query
            tag_str = tag_str[8:]
            tag_str = tag_str.replace("%20"," ")
            tags = tag_str.split("  ")
            point = 0
            if(len(tags)==3):
                point = 100 * (self.points[tags[0]] + self.points[tags[1]] + self.points[tags[2]] +2)/(3.0 * self.n_queries)
            else:
                point = 100 * (self.points[tags[0]] + self.points[tags[1]])/(2.0 * self.n_queries)
            title = title.replace('"', '')
            typ = "Webpage"
            if("pdf" in url):
                typ = "Document"
            elif("youtube" in url):
                typ = "Youtube video"
            elif("wikipedia" in url):
                typ = "Wiki"
            yield {'search url' : response.url, 'url' : parsed_url, 'description' : desc, 'tags' : tags, 'title' : title, 'type' : typ, 'score' : round(point,1)}
