# -*- coding: utf-8 -*-
import scrapy
#from scrap_tatainnoverse.items import ScrapTatainnoverseItem
from scrapy.crawler import CrawlerProcess


class ScrapChallengeDescSpider(scrapy.Spider):
    name = 'scrap_challenge_desc'
    base_url = "http://www.tatainnoverse.com/"
    start_urls = ['http://www.tatainnoverse.com/index.php//']

    def parse(self, response):
        for challenge_link in  response.css("section#openchallenges div.content h3 a::attr(href)").extract():
            #yield { (challenge_link.split("="))[1] : challenge_link}
            yield scrapy.Request(self.base_url+challenge_link, callback = self.parse_desc)
    def parse_desc(self, response):
        desc = response.xpath(".//*[@id='singlechallengedesc']").xpath("string()").extract()
        title = response.css("div.container h1::text").extract_first()
    	res = {}
    	res["_id"] = (response.url.split("="))[1]
    	res["content"] = desc[0]
        res["title"] = title
        yield res

'''process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

crawl = process.crawl(ScrapChallengeDescSpider)
run = process.start'''
