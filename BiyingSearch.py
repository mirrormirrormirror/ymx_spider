from bs4 import BeautifulSoup
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import requests
import re
from KeywordDao import KeywordDao
from DetailLinkDao import DetailLinkDao
import pymysql
import redis
from selenium import webdriver
from SlpLinkDao import SlpLinkDao
import time


class SearchBiying:

    def __init__(self):
        # print('google init')
        self.baseSearchUrl = 'https://cn.bing.com/search?q=site: amazon.com /slp/ %s currently unavailable&go=Search&qs=ds&first=%s&FORM=PERE2'
        self.keywordDao = KeywordDao()
        print('init keywordDao finish')
        self.detailLinkDao = DetailLinkDao()
        print('init detailLinkDao finish')
        self.slpLinkDao = SlpLinkDao()
        print('init slpLinkDao finish')

        self.exitsPageCount = 0

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('window-size=1920x3000')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')

        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"')


        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--proxy-server=%s' % 'https://127.0.0.1:8388')
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.driver.set_page_load_timeout(10)
        # self.driver.implicitly_wait(20)
        self.driver.get('https://cn.bing.com/?mkt=zh-CN')
        # print(self.driver.page_source)
        # print(self.driver.page_source)

        self.myRedis = redis.Redis(host='localhost', port=6379, db=0)
        self.googleHost = 'google_host'

    def getKeyword2link(self, keywordId, allLinks):
        keywordId2link = list()

        for link in allLinks:
            keywordId2link.append((link, keywordId))
        return keywordId2link

    def getDownloadLink(self, keyword, pageNum):
        print('getDownloadLink ----')
        # print(self.baseSearchUrl % ('https://www.google.com', keyword, pageNum * 10))
        # print('getDownloadLink----')
        # host = self.myRedis.srandmember(self.googleHost)
        return self.baseSearchUrl % (keyword, pageNum * 10 + 1)

    def parsePageLink(self, text):
        # pattern = 'https://www.amazon.ca/[a-zA-Z0-9-]+/dp/[a-zA-Z0-9]+'
        pattern = 'https://www.amazon.ca/slp/([a-zA-Z0-9-]+/?)+'
        pageLinks = re.findall(pattern, text)
        print('page link:'+str(pageLinks))
        result = set()
        for i in pageLinks:
            result.add('https://www.amazon.ca/slp/' + i)
        return result

    def download(self, url):
        page = requests.get(url)
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
        if 'sb_pagN sb_pagN_bp b_widePag sb_bp' in text and '404 Charity' not in text:
            return False
        else:
            return True

    def run(self, keywordId2Keyword):

        print('run---')
        keyword = keywordId2Keyword[1]
        keywordId = keywordId2Keyword[0]
        text = self.sentKey(keyword)
        pageLinks = self.parsePageLink(text)
        pageLinks = self.slpLinkDao.removalDuplicate(pageLinks)
        if len(pageLinks) == 0:
            print('Duplicate page')
            self.exitsPageCount = self.exitsPageCount + 1


        print('pageLinks:' + str(pageLinks))
        keyword2slpLink = self.getKeyword2link(keywordId, pageLinks)
        self.keywordDao.updateKeywordState(keywordId, 2)
        self.slpLinkDao.batchInsert(keyword2slpLink)
        isLastPage = self.isLastPage(text)
        print('one page isLastPage:' + str(isLastPage))
        nextPage = text
        while not isLastPage:
            if self.exitsPageCount > 2:
                print('Duplicate keyword skip--')
                break

            nextPage = self.clikNext(nextPage)
            if nextPage is None:
                isLastPage = True
                continue
            nextPageLinks = self.parsePageLink(nextPage)
            nextPageLinks = self.slpLinkDao.removalDuplicate(nextPageLinks)
            print('nextPageLinks:' + str(nextPageLinks))

            if len(nextPageLinks) == 0:
                print('Duplicate page next')
                self.exitsPageCount = self.exitsPageCount + 1

            # print('next page link:' + str(nextPageLinks))
            keywordId2nextPageLink = self.getKeyword2link(keywordId, nextPageLinks)
            self.slpLinkDao.batchInsert(keywordId2nextPageLink)
            self.keywordDao.updateKeywordState(keywordId, 2)
            isLastPage = self.isLastPage(nextPage)
            print('next page isLastPage:' + str(isLastPage))

    def close(self):
        self.keywordDao.close()
        self.myRedis.close()
        self.driver.close()
        self.driver.quit()

    def sentKey(self, keyword):
        print('sent key')
        key = 'site: amazon.ca /slp/ %s currently unavailable' % keyword
        print(key)
        self.driver.find_element_by_css_selector('#sb_form_q').send_keys(key)
        self.driver.find_element_by_css_selector('#sb_form_go').click()
        print('sent key finish')
        time.sleep(3)
        # self.driver.find_element_by_css_selector('#est_cn').click()
        # time.sleep(5)
        text = self.driver.page_source
        print('page_source finish')

        return text

    def clikNext(self, nextPage):

        nextPageSoup = BeautifulSoup(nextPage)
        try:
            nextPageLink = nextPageSoup.select('#b_results > li.b_pag > nav > ul > li .sb_pagN')[0]['href']
        except:
            return None
        self.driver.get('https://cn.bing.com/' + nextPageLink)

        # print('clikNext')
        # # self.driver.find_element_by_css_selector('.sw_next').click()
        # self.driver.find_element_by_partial_link_text('2').click()
        time.sleep(3)
        text = self.driver.page_source
        # print('next text:'+text)
        return text


if __name__ == '__main__':

    while True:
        detailLinkDao = DetailLinkDao()
        keyWordDao = KeywordDao()
        try:
            searchBiying = SearchBiying()
        except:
            print('search init fail')
            searchBiying.close()
        try:
            # try:
            id2keyword = keyWordDao.popKeyWordForRedis()
            print(id2keyword)
            print(time)
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
                searchBiying.run(id2keywordDic)
        except Exception as e:
            print(e)
        finally:
            try:
                searchBiying.close()
            except:
                print("searchBiying.close() fail")


