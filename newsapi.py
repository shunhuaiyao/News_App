import sys
import time
import json
import jieba
import jieba.analyse
import operator
import requests

def longestCommonPrefix(keywords):
        """
        :type strs: list[str]
        :rtype: str
        """
        if len(keywords) == 0:
            return ""
        commonPrefix = keywords[0]
        for string in keywords:
            while string.find(commonPrefix) != 0:
                commonPrefix = commonPrefix[:(len(commonPrefix)-1)]
                if len(commonPrefix) == 0:
                    return ""
        return commonPrefix

'''
google news api:
title string may be divided by '|' and '-'
'''

def listDailyKeyword(news):
    for article in news['articles']:
        title = article['title']
        descriptions = article['description'].split()[0]
        if '|' in title:
            title = title[:title.find('|')]
        if '-' in title:
            title = title[:title.find('-')]
        allWords = jieba.analyse.extract_tags(title, topK=20, withWeight=False, allowPOS=())
        allWords = allWords + jieba.analyse.extract_tags(descriptions, topK=40, withWeight=False, allowPOS=())
        # allWords = allWords + jieba.analyse.extract_tags(title, topK=20, withWeight=False, allowPOS=('n'))
        # allWords = allWords + jieba.analyse.extract_tags(descriptions, topK=40, withWeight=False, allowPOS=('n'))
        
        lookup = dict()
        for word in allWords:
            lookup[word] = lookup.get(word, 0) + 1
        keywords = list(lookup.keys())
        for i, keyword1 in enumerate(keywords):
            for j, keyword2 in enumerate(keywords):
                if i == j:
                    continue
                commonPrefix = longestCommonPrefix(list([keyword1, keyword2]))
                if len(commonPrefix) >= 2:
                    lookup[commonPrefix] = lookup.get(keyword1, 0) + lookup.get(keyword2, 0)

        lookup = sorted(lookup.items(), key=operator.itemgetter(1), reverse=True)
        
        keywords = ''
        for keyword in lookup[:5]:
            if '...' in keyword:
                continue
            keywords += keyword[0] + ' '
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
    # date = '2019-01-16'
    news = crawlNews(google_base_api+api_key, google_domainQuery+domains, google_date_startQuery+date, google_date_endQuery+date, google_sortingQuery+"popularity", google_pageSizeQuery, google_pageQuery)
    # print(news.keys())
    # for article in news["articles"]:
    #     print(article["title"])
    # print(len(news["articles"]))
    # print(news["articles"][0])
    listDailyKeyword(news)