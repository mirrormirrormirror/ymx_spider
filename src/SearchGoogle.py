import requests
import re
from src.KeywordDao import KeywordDao
from src.DetailLinkDao import DetailLinkDao
import pymysql
import redis
from src.SlpLinkDao import SlpLinkDao
import time


class SearchGoogle:

    def __init__(self):
        print('google init')
        self.baseSearchUrl = '%s/search?sxsrf=ACYBGNQijJp1zP8DrIYLxxx7uIToLlL4mw:1574336804346&ei=JHnWXdDgFOPFmAWp9rW4DA&q=inurl:www.amazon.ca/slp %s currently unavailable&start=%s'
        self.keywordDao = KeywordDao()
        print('init keywordDao finish')
        self.detailLinkDao = DetailLinkDao()
        print('init detailLinkDao finish')
        self.slpLinkDao = SlpLinkDao()
        print('init slpLinkDao finish')


        self.downloadCount = 0
        self.downloadCountPoint = 0

        self.myRedis = redis.Redis(host='localhost', port=6379, db=0)
        self.googleHost = 'google_host'

    def getKeyword2link(self, keywordId, allLinks):
        keywordId2link = list()

        for link in allLinks:
            keywordId2link.append((link, keywordId))
        return keywordId2link

    def getDownloadLink(self, keyword, pageNum):
        print('getDownloadLink ----')
        print(self.baseSearchUrl % ('https://www.google.com', keyword, pageNum * 10))
        # print('getDownloadLink----')
        # host = self.myRedis.srandmember(self.googleHost)
        return self.baseSearchUrl % ('http://www.google.com', keyword, pageNum * 10)

    def parsePageLink(self, text):
        # pattern = 'https://www.amazon.ca/[a-zA-Z0-9-]+/dp/[a-zA-Z0-9]+'
        pattern = 'https://www.amazon.ca/slp/([a-zA-Z0-9-]+/?)+'
        pageLinks = re.findall(pattern, text)
        result = []
        for i in pageLinks:
            result.append('https://www.amazon.ca/slp/' + i)
        return result

    def download(self, url):
        # text = requests.get(url).text

        session = requests.session()
        session.get('https://www.google.com/search?sxsrf=ACYBGNQijJp1zP8DrIYLxxx7uIToLlL4mw%3A1574336804346&ei=JHnWXdDgFOPFmAWp9rW4DA&q=python+requests+proxy&oq=python+requests+pro&gs_l=psy-ab.3.0.0j0i203l4j0j0i203j0j0i203j0.699.1661..3205...0.2..0.940.2238.3-1j1j1j1......0....1..gws-wiz.......0i71j35i39j0i67.YEgpl36LGxI')
        page = session.get(url)
        text = page.text

        print(page.status_code)
        return text

    def iniHostToRedis(self):
        db = pymysql.connect(host='localhost', user='root', password='mirror123', database='ymx')
        cursor = db.cursor()
        cursor.execute('select google_host from t_ymx_google_host')
        data = cursor.fetchall()
        for row in data:
            self.myRedis.sadd(self.googleHost, str(row[0]))

    def isLastPage(self, text):
        if 'pnnext' in text:
            return False
        else:
            return True

    def run(self, keywordId2Keyword):
        print('run---')
        keyword = keywordId2Keyword[1]
        keywordId = keywordId2Keyword[0]
        # 获取第一页
        url = self.getDownloadLink(keyword, 0)
        print('one page link:' + url)
        text = self.download(url)
        pageLinks = self.parsePageLink(text)
        keyword2slpLink = self.getKeyword2link(keywordId, pageLinks)
        self.keywordDao.updateKeywordState(keywordId, 2)
        self.slpLinkDao.batchInsert(keyword2slpLink)
        isLastPage = self.isLastPage(text)
        print('one page isLastPage:' + str(isLastPage))

        pageNum = 1
        while not isLastPage:
            nextPage = self.getDownloadLink(keyword, pageNum)
            print('next page link:' + nextPage)
            nextPageLinks = self.parsePageLink(nextPage)
            print('next page link:' + str(nextPageLinks))
            keywordId2nextPageLink = self.getKeyword2link(keywordId, nextPageLinks)
            self.slpLinkDao.batchInsert(keywordId2nextPageLink)
            self.keywordDao.updateKeywordState(keywordId, 2)
            isLastPage = self.isLastPage(text)
            print('next page isLastPage:' + str(isLastPage))
            if not isLastPage:
                pageNum = pageNum + 1

    def close(self):
        self.keywordDao.close()
        self.detailLinkDao.close()
        self.myRedis.close()
        # self.chrome.close()


if __name__ == '__main__':

    while True:
        detailLinkDao = DetailLinkDao()
        keyWordDao = KeywordDao()
        try:
            id2keyword = keyWordDao.popKeyWordForRedis()
            print(id2keyword)

            print(time.strftime(' %Y-%m-%d %H:%M:%S %p %w ', time.localtime(time.time())))
            if id2keyword is None:
                print('no keyword stop 3 second')
                time.sleep(3)
                continue
            else:
                print('go to run keyword')
                id2keywordDic = eval(id2keyword)
                print(id2keywordDic)
                keyWord = id2keywordDic[1]
                print(keyWord)
                keywordId = id2keywordDic[0]
                print(keywordId)
                googleSearch = SearchGoogle()
                googleSearch.run(id2keywordDic)
            keyWordDao.close()
            detailLinkDao.close()

        except:
            keyWordDao.close()
            detailLinkDao.close()
