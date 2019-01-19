import time
import requests
from bs4 import BeautifulSoup

ltn_nonsensKeywords = ['自由時報', '自由電子報', '自由時報電子報', '自由娛樂', '自由體育', 'libertytimes', 'Liberty Times Net', 'ltn', 'LTN', '自由評論網', '自由共和國', '自由限時批', '國內要聞', '國際快訊']

def getResponse(url):
    responds = requests.get(url)
    responds.encoding = 'utf-8'
    soup = BeautifulSoup(responds.content, "lxml")
    return soup

def crawlLtnNews(breaking, ltnNews_base, ltnBreakingNews_list, ltnNewsPaper_list, category, date):
    url = ltnNews_base
    if breaking:
        url += ltnBreakingNews_list
    else:
        url += ltnNewsPaper_list + category + date
    # get into article lists
    soup = getResponse(url)
    pageNum = 1
    # if the number of pages is larger than 2, class 'p_last' will exist.
    pagination = soup.find(name='a', attrs={'class': 'p_last'})
    if pagination:
        pageNum = int(str(pagination.get('href')).split('/')[-1])
    for page in range(pageNum):
        # get into articles in one page
        print('Page:', str(page+1))
        soup = getResponse(url+str(page+1))
        articles = soup.find_all(name='a', attrs={'class': 'ph'})
        for article in articles:
            # get into the article to parse details
            title = str(article.get('data-desc')).split(':')[-1]
            suffix = str(article.get('href'))
            Id = suffix.split('/')[-1]
            print('Title:', title, 'Id:', Id)
            # get thumbnail url for the article
            img = ''
            if article.find(name='img'):
                img = article.find(name='img').get('src')
            print('Image Url:', img)
            if breaking:
                article_url = 'http:' + suffix
            else:
                article_url = ltnNews_base + suffix
            print('URL:', article_url)
            # get into one article
            soup = getResponse(article_url)
            # get published date from meta or span
            date = ''
            if soup.find(name='meta', attrs={'name': 'pubdate'}):
                date = str(soup.find(name='meta', attrs={'name': 'pubdate'}).get('content'))
            elif soup.find(name='span', attrs={'class': 'time'}):
                date = soup.find(name='span', attrs={'class': 'time'}).string
            print('Date:', date)
            # get keywords from meta
            keywords = str(soup.find(name='meta', attrs={'name': 'keywords'}).get('content')).split(',')
            non_keywords = list()
            for keyword in keywords:
                if keyword.strip() in ltn_nonsensKeywords:
                    non_keywords.append(keyword)
            for non_keyword in non_keywords:
                keywords.remove(non_keyword)
            print('Keywords:', keywords)
            # get description from meta
            description = str(soup.find(name='meta', attrs={'name': 'description'}).get('content')).split('。')[0]
            if '\n' in description:
                description = description.split('\n')[-1]
            print('Description:', description)
            # get contents
            if soup.find(name='div', attrs={'itemprop': 'articleBody'}):
                contents_div = soup.find(name='div', attrs={'itemprop': 'articleBody'})
            else:
                contents_div = soup.find(name='div', attrs={'class': 'text'})
            contents = contents_div.find_all(name='p', attrs={'class': None})
            allContents = ''
            for content in contents:
                if content.string:
                    allContents += content.string
            print('Contents:', allContents)

if __name__ == '__main__':
    breaking = False
    ltnNews_base = 'http://news.ltn.com.tw/'
    ltnBreakingNews_list = 'list/breakingnews/all/'
    ltnNewsPaper_list = 'list/newspaper/'
    categories = ['focus/', 'politics/', 'society/', 'local/', 'life/', 'opinion/', 'world/', 'business/', 'sports/', 'entertainment/', 'consumer/']
    date = time.strftime('%Y%m%d/')
    crawlLtnNews(breaking, ltnNews_base, ltnBreakingNews_list, ltnNewsPaper_list, categories[0], date)


