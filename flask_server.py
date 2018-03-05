#import scrapy
#from scrapy.crawler import CrawlerRunner
#from scrapy.utils.project import get_project_settings
from flask import Flask, jsonify, request
import subprocess
from rake_nltk import Rake
import random
import string
from datetime import datetime
import timeit

app = Flask(__name__)


@app.route("/refresh", methods=['GET'])
def refresh():
    '''process = CrawlerRunner( get_project_settings() )
    process.crawl('scrap_challenge_desc')
    process.start()'''
    subprocess.check_output(['scrapy', 'crawl', 'spider1'])
    return ""

@app.route("/final", methods=['POST'])
def final():
    arg = request.get_json()
    keyword_scores = arg['keyword_scores']
    time_limit = str(arg['time_limit'])
    keyword_scores = sorted(keyword_scores.iteritems(), key=lambda (k,v): (v,k), reverse=True)
    file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(12))

    concatenated_keywords = ""
    for i in range(len(keyword_scores)-1):
        concatenated_keywords = concatenated_keywords + keyword_scores[i][0] + ","
    concatenated_keywords = concatenated_keywords + keyword_scores[len(keyword_scores)-1][0]

    start_time = timeit.default_timer()
    flag = random.randint(1,2)
    if(flag==1):
        print "google"
        subprocess.call(['timeout',time_limit,'scrapy', 'crawl', 'spider2', '-a', 'query='+concatenated_keywords, '-o', 'temp/'+file_name+'.json'])
    else:
        print "bing"
        subprocess.call(['timeout',time_limit,'scrapy', 'crawl', 'spider3', '-a', 'query='+concatenated_keywords, '-o', 'temp/'+file_name+'.json'])
    elapsed = timeit.default_timer() - start_time

    print elapsed/len(keyword_scores)

    return file_name

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
