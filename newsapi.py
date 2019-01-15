import sys
import time
import jieba
import requests

def crawlNews(url, domainsQuery, startQuery, endQuery, sortingQuery):
    api_url = url + domainsQuery + startQuery + endQuery + sortingQuery
    r = requests.get(api_url)
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
    configFile = sys.argv[1]
    api_key, domains = readConfigFile(configFile)
    date = time.strftime("%Y-%m-%d")
    news = crawlNews(google_base_api+api_key, google_domainQuery+domains, google_date_startQuery+date, google_date_endQuery+date, google_sortingQuery+"popularity")
    print(news)