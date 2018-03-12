# -*- coding: utf-8 -*-
import scrapy
import re
import cgi
from urlparse import urljoin, urlparse, parse_qsl

class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    base_url = "http://www.tatainnoverse.com/"
    start_urls = ['http://www.tatainnoverse.com/season1.php/' ,
    'http://www.tatainnoverse.com/season2.php/',
    'http://www.tatainnoverse.com/season3.php/',
    'http://www.tatainnoverse.com/season4.php/',
    'http://www.tatainnoverse.com/season5.php/',
    'http://www.tatainnoverse.com/season6.php/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.MongoPipeline': 300,
            },
        'CONCURRENT_REQUESTS' : 32,
        'DOWNLOAD_DELAY' : 0
        }

    def parse(self, response):
        if(response.status==200):    
            for challenge_link in  response.css(".singlebox a::attr(href)").extract():
                #yield { (challenge_link.split("="))[1] : challenge_link}
                yield scrapy.Request(self.base_url+challenge_link, callback = self.parse_desc)
    def parse_desc(self, response):
        description = response.xpath(".//*[@id='singlechallengedesc']").xpath("string()").extract()
        title = response.css("div.container h1::text").extract_first()
        html = response.css("#singlechallengedesc").extract_first()
        title = title.replace("\t", "")
        desc = description[0]
        desc = desc.replace("\n", " ")
        desc = desc.replace("\t", "")
        desc = desc.replace("\r", "")
        desc = desc.lstrip()
        desc = desc.rstrip()
        html = html.replace("\n", " ")
        html = html.replace("\t", "")
        html = html.replace("\r", "")
        html = re.sub(r'<img\s+[^>]*src="([^"]*)"[^>]*>', '', html)
        html = cgi.escape(html).encode('ascii', 'xmlcharrefreplace')
        html = html.replace('&lt;',"<")
        html = html.replace('&gt;',">")
        html = html.replace('&amp;',"&")
        html = re.sub(r'(?s)<span.*?>',' ', html)
        html = re.sub(r'(?s)</span>',' ', html)
        desc = re.sub(r'[\(\[].*?[\)\]]', "", desc)
        desc = desc.replace("[", "")
        desc = desc.replace("]", "")
        desc = desc.replace("(", "")
        desc = desc.replace(")", "")
        desc = re.sub(r'\\[a-z, 0-9]*', "", desc)
        desc = re.sub(r'[0-9]*', "", desc)
        desc = re.sub(r'http[a-z,:,/,.,-]*', "",  desc)
        query = urlparse(response.url).query
        _id, status = query.split("&")

        res = {}
    	res["_id"] = (_id.split("="))[1]
        res["status"] = (status.split("="))[1]
    	res["content"] = desc
        res["title"] = title
        res["url"] = response.url
        res["html"] = html
        yield res
