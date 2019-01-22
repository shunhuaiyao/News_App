import time
import requests
from bs4 import BeautifulSoup

categories = ['政治', '社會', '生活', '國際', '財經', '體育', '娛樂', '科技']

def getResponse(url):
    responds = requests.get(url)
    responds.encoding = 'utf-8'
    soup = BeautifulSoup(responds.content, "lxml")
    return soup

def crawlChinaTimesNews(chinatimesNews_base, chinatimesBreakingNews_list):
    # get into article lists
    url = chinatimesNews_base + chinatimesBreakingNews_list
    page = 1
    soup = getResponse(url+str(page))
    pagination = soup.find(name='div', attrs={'class': 'pagination clear-fix'}).find_all(name='li', attrs={'class': None})[-1]
    pageNum = int(str(pagination.find(name='a').get('href')).split('=')[-1])
    for page in range(pageNum):
        # get into articles in one page
        print('Page:', str(page+1))
        soup = getResponse(url+str(page+1))
        article_list = soup.find(name='div', attrs={'class': 'listRight'}).find_all(name='li', attrs={'class': 'clear-fix'})
        for article in article_list:
            # get article's Id, category, article_url, title, and date
            Id = str(article.find(name='h2').find(name='a').get('href')).split('/')[-1]
            article_url = chinatimesNews_base + article.find(name='h2').find(name='a').get('href')
            title = str(article.find(name='h2').get_text()).strip()
            date = article.find(name='time').get('datetime')
            category = str(article.find(name='div', attrs={'class': 'kindOf'}).get_text()).strip()
            if category == '兩岸':
                category = '國際'
            elif category not in categories:
                category = '其他'
            print(Id, category, article_url, title, date)
            # get into one article
            soup = getResponse(article_url)
            # get description from meta
            description = ''
            description_meta = soup.find(name='meta', attrs={'name': 'description'})
            if description_meta:
                description = description_meta.get('content')
            # get keywords from meta
            keywords = ''
            keywords_meta = soup.find(name='meta', attrs={'name': 'keywords'})
            if keywords_meta:
                keywords = keywords_meta.get('content')
            # get thumbnail from meta
            img = ''
            img_meta = soup.find(name='meta', attrs={'name': 'image'})
            if img_meta:
                img = img_meta.get('content')
            print(keywords, img, description)
            # get contents
            contents = soup.find(name='article', attrs={'class': 'arttext marbotm clear-fix'}).find_all(name='p', attrs={'class': None})
            allContents = ''
            for content in contents:
                if content.get_text():
                    allContents += content.get_text()
            print('Contents:', allContents)


if __name__ == "__main__":
    chinatimesNews_base = 'https://www.chinatimes.com'
    chinatimesBreakingNews_list = '/realtimenews/?page='
    crawlChinaTimesNews(chinatimesNews_base, chinatimesBreakingNews_list)