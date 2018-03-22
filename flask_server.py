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
import textacy
from textacy import keyterms
from collections import Counter
import operator
#import spacy
#spacy.load('en_core_web_sm')


app = Flask(__name__)


@app.route("/refresh", methods=['GET'])
def refresh():
    subprocess.check_output(['scrapy', 'crawl', 'spider1'])
    return ""


@app.route("/final", methods=['POST'])
def final():
    arg = request.get_json()
    keywords = arg['keywords']
    time_limit = str(arg['time_limit'])
    engine = str(arg['engine'])
    file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(12))


    concatenated_keywords = ""
    for i in range(len(keywords)-1):
        concatenated_keywords = concatenated_keywords + keywords[i] + ","
    concatenated_keywords = concatenated_keywords + keywords[len(keywords)-1]

    print concatenated_keywords,engine,time_limit


    '''
    start_time = timeit.default_timer()
    flag = random.randint(1,2)
    if(flag==1):
        print "google"
        subprocess.call(['timeout',time_limit,'scrapy', 'crawl', 'spider2', '-a', 'query='+concatenated_keywords, '-o', 'temp/'+file_name+'.json'])
    else:
        print "bing"
        subprocess.call(['timeout',time_limit,'scrapy', 'crawl', 'spider3', '-a', 'query='+concatenated_keywords, '-o', 'temp/'+file_name+'.json'])
    elapsed = timeit.default_timer() - start_time
    print elapsed/len(keyword_scores)'''

    if(engine=='on'):
        subprocess.call(['timeout',time_limit,'scrapy', 'crawl', 'spider2', '-a', 'query='+concatenated_keywords, '-o', 'temp/'+file_name+'.json'])
    else:
        subprocess.call(['timeout',time_limit,'scrapy', 'crawl', 'spider3', '-a', 'query='+concatenated_keywords, '-o', 'temp/'+file_name+'.json'])

    #subprocess.call(['timeout',time_limit,'scrapy', 'crawl', 'spider2', '-a', 'query='+concatenated_keywords, '-o', 'temp/'+file_name+'.json'])
    return file_name



'''@app.route("/final", methods=['POST'])
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



    #subprocess.call(['timeout',time_limit,'scrapy', 'crawl', 'spider2', '-a', 'query='+concatenated_keywords, '-o', 'temp/'+file_name+'.json'])
    return file_name
'''

temp = textacy.Doc(unicode('temp') , lang=unicode('en_core_web_sm'))
@app.route("/keywords", methods=['POST'])
def keywords():
    #print request.get_json()
    arg = request.get_json()
    doc = textacy.Doc(arg['content'] , metadata = {'title' : arg['title']}, lang=unicode('en_core_web_sm'))
    sgrank_keywords = dict(keyterms.sgrank(doc))
    singlerank_keywords = dict(keyterms.singlerank(doc))
    textrank_keywords = dict(keyterms.textrank(doc))
    sgrank_keywords.update((x, y*0.9) for x, y in sgrank_keywords.items())
    textrank_keywords.update((x, y*0.05) for x, y in textrank_keywords.items())
    singlerank_keywords.update((x, y*0.05) for x, y in singlerank_keywords.items())
    keywords = res = dict(Counter(sgrank_keywords) + Counter(textrank_keywords) + Counter(singlerank_keywords))
    sorted_keywords = sorted(keywords.items(), key=operator.itemgetter(1), reverse=True)
    keyword_string = ""

    for i,key in enumerate(sorted_keywords):
        if(i==int(len(sorted_keywords)/2)):
            keyword_string = keyword_string + "||"
        if(i==len(sorted_keywords)-1 or i==int(len(sorted_keywords)/2)-1):
            keyword_string = keyword_string + key[0]
        else:
            keyword_string = keyword_string + key[0] + ",,"

    return keyword_string


if __name__ == '__main__':
    app.run(debug=True)
