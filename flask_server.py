import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import scrap_tatainnoverse
from flask import Flask, jsonify, request
import subprocess
from rake_nltk import Rake

app = Flask(__name__)


@app.route("/refresh", methods=['GET'])
def refresh():
    '''process = CrawlerRunner( get_project_settings() )
    process.crawl('scrap_challenge_desc')
    process.start()'''
    subprocess.check_output(['scrapy', 'crawl', 'spider1'])
    return ""

@app.route("/keywords", methods=['POST'])
def keywords():
    #print request.get_json()
    arg = request.get_json()
    r = Rake()
    r.extract_keywords_from_text(arg['content'])
    content_keywords = r.get_ranked_phrases()
    r.extract_keywords_from_text(arg['title'])
    title_keywords = r.get_ranked_phrases()
    top_keywords = ""
    n_keywords = 10
    for i in range(2):
        top_keywords = top_keywords + title_keywords[i] + ",,"
    for i in range(n_keywords):
        if(i==n_keywords-1):
            top_keywords  = top_keywords + content_keywords[i]
        else:
            top_keywords  = top_keywords + content_keywords[i] + ",,"

    top_keywords  = top_keywords + "||"

    for i in range(n_keywords, n_keywords + 10):
        if(i == n_keywords + 9 or i == len(content_keywords)-1):
            top_keywords = top_keywords + content_keywords[i]
            break
        else:
            top_keywords  = top_keywords + content_keywords[i] + ",,"

    return top_keywords



if __name__ == '__main__':
    app.run(debug=True)
