import sys
import time
import json
import jieba
import jieba.analyse
import requests

'''
google news api:
title string may be divided by '|' and '-'
'''

def listDailyKeyword(news):
    for article in news['articles']:
        title = article['title']
        if '|' in title:
            title = title[:title.find('|')]
        if '-' in title:
            title = title[:title.find('-')]
        # sentence = title+'。'+article['description']
        nouns = jieba.analyse.extract_tags(title, topK=2, withWeight=False, allowPOS=())
        verbs = jieba.analyse.extract_tags(title, topK=2, withWeight=False, allowPOS=('v'))
        keywords = nouns + verbs
        print(title)
        print(keywords)
    

def crawlNews(url, domainsQuery, startQuery, endQuery, sortingQuery, pageSizeQuery, pageQuery):
    api_url = url + domainsQuery + startQuery + endQuery + sortingQuery + pageSizeQuery + pageQuery
    r = requests.get(api_url)
    print(api_url)
    return r.json()
    
def readConfigFile(fileName):
    with open(fileName) as f:
        content = f.readlines()
        for config in content:
            if "GoogleNewsAPIKey" in config.strip().split()[0]:
                api_key = config.strip().split()[1]
            elif "searchDomains" in config.strip().split()[0]:
                domains = config.strip().split()[1]
    return api_key, domains
if __name__ == "__main__":
    google_base_api = "https://newsapi.org/v2/everything?apiKey="
    google_domainQuery = "&domains="
    google_date_startQuery = "&from="
    google_date_endQuery = "&to="
    google_sortingQuery = "&sortBy="
    google_pageSizeQuery = "&pageSize=100"
    google_pageQuery = "&page=1"
    configFile = sys.argv[1]
    api_key, domains = readConfigFile(configFile)
    date = time.strftime("%Y-%m-%d")
    news = crawlNews(google_base_api+api_key, google_domainQuery+domains, google_date_startQuery+date, google_date_endQuery+date, google_sortingQuery+"popularity", google_pageSizeQuery, google_pageQuery)
    # print(news.keys())
    # for article in news["articles"]:
    #     print(article["title"])
    # print(len(news["articles"]))
    # print(news["articles"][0])
    listDailyKeyword(news)