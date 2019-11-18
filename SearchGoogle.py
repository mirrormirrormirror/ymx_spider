import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from KeywordDao import KeywordDao
from DetailLinkDao import DetailLinkDao


class SearchGoogle:

    def __init__(self):
        self.baseSearchUrl = 'https://www.google.com/search?q=site:amazon.ca %s currently unavailable&start=%s'
        self.keywordDao = KeywordDao()
        self.detailLinkDao = DetailLinkDao()

    def getKeyword2link(self, keywordId, allLinks):
        keywordId2link = list()

        for link in allLinks:
            keywordId2link.append((link, keywordId))
        return keywordId2link

    def getDownloadLink(self, keyword, pageNum):
        return self.baseSearchUrl % (keyword, pageNum * 10)

    def parsePageLink(self, text):
        pattern = 'https://www.amazon.ca/[a-zA-Z0-9-]+/dp/[a-zA-Z0-9]+'
        pageLinks = re.findall(pattern, text)
        return pageLinks

    def download(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(u'返回状态码异常：'+str(response.status_code))
            return None

    def getPageLink(self, keyword, pageNum):
        pass

    def isLastPage(self, text):
        if 'pnnext' in text:
            return True
        else:
            return False

    def run(self, keywordId2Keyword):
        keyword = keywordId2Keyword[1]
        keywordId = keywordId2Keyword[0]
        # 获取第一页
        url = self.getDownloadLink(keyword, 0)
        text = self.download(url)
        pageLinks = self.parsePageLink(text)
        keyword2link = self.getKeyword2link(keywordId, pageLinks)
        self.keywordDao.updateKeywordState(keywordId, 2)
        self.detailLinkDao.batchInsert(keyword2link)
        isLastPage = self.isLastPage(text)
        pageNum = 1
        while not isLastPage:
            nextPage = self.getDownloadLink(keyword, pageNum)
            nextPageLinks = self.parsePageLink(nextPage)
            keywordId2nextPageLink = self.getKeyword2link(keywordId, nextPageLinks)
            self.detailLinkDao.batchInsert(keywordId2nextPageLink)
            self.keywordDao.updateKeywordState(keywordId, 2)
            isLastPage = self.isLastPage(text)
            if not isLastPage:
                pageNum = pageNum + 1

    def close(self):
        self.keywordDao.close()
        self.detailLinkDao.close()


if __name__ == '__main__':

    while True:
        detailLinkDao = DetailLinkDao()
        keyWordDao = KeywordDao()
        try:
            id2keyword = keyWordDao.popKeyWordForRedis()
            if id2keyword is None:
                print(u'关键词没了，睡眠3秒')
                continue
            else:
                id2keywordDic = eval(id2keyword)
                keyWord = id2keywordDic[1]
                keywordId = id2keywordDic[0]
                googleSearch = SearchGoogle()
                googleSearch.run(id2keywordDic)
            keyWordDao.close()
            detailLinkDao.close()
        except:
            keyWordDao.close()
            detailLinkDao.close()
