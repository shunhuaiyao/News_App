import time
import requests
from bs4 import BeautifulSoup

categories = ['政治', '社會', '生活', '論壇', '國際', '財經', '體育', '娛樂', '3C']

def getResponse(url):
    responds = requests.get(url)
    responds.encoding = 'utf-8'
    soup = BeautifulSoup(responds.content, "lxml")
    return soup

def crawlAppleNews(appleNews_base, appleBreakingNews_list):
    # get into article lists
    url = appleNews_base + appleBreakingNews_list
    pages = 1
    for page in range(pages):
        soup = getResponse(url+str(page+1))
        article_lists = soup.find_all(name='ul', attrs={'class': 'rtddd slvl'})
        for article_list in article_lists:
            articles = article_list.find_all(name='li')
            for article in articles:
                # get article's url, id, and category
                article_url = str(article.find(name='a').get('href'))
                Id = article_url.split('/')[-2]
                category = article.find(name='h2').string
                if category not in categories:
                    category = '其他'
                # get into one article
                soup = getResponse(article_url)
                article_info = soup.find(name='hgroup', attrs={'class': None})
                title = article_info.find(name='h1').string
                date = str(article_info.find(name='div', attrs={'class': 'ndArticle_creat'}).text).split('：')[-1]
                print(article_url, Id, category, title, date)
                # get img, keywords and description from meta
                img = soup.find(name='meta', attrs={'property': 'og:image'}).get('content')
                keywords = str(soup.find(name='meta', attrs={'name': 'keywords'}).get('content'))
                description = soup.find(name='meta', attrs={'name': 'description'}).get('content')
                print(img, keywords, description)
                # get content
                contents_div = soup.find(name='div', attrs={'class': 'ndArticle_margin'})
                contents = contents_div.find(name='p', attrs={'class': None}).get_text()
                print(contents)

if __name__ == "__main__":
    appleNews_base = 'https://tw.appledaily.com/'
    appleBreakingNews_list = 'new/realtime/'
    crawlAppleNews(appleNews_base, appleBreakingNews_list)
