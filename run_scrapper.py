import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrap_tatainnoverse


process = CrawlerProcess( get_project_settings() )
process.crawl('scrap_challenge_desc')
process.start()
