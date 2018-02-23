import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import scrap_tatainnoverse
from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)


@app.route("/refresh", methods=['GET'])
def refresh():
    '''process = CrawlerRunner( get_project_settings() )
    process.crawl('scrap_challenge_desc')
    process.start()'''
    subprocess.check_output(['scrapy', 'crawl', 'scrap_challenge_desc'])
    return ""



if __name__ == '__main__':
    app.run(debug=True)
