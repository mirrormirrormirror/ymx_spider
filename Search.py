#coding=utf8
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from KeywordDao import KeywordDao
from DetailLinkDao import DetailLinkDao


class Search:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.driver = webdriver.PhantomJS('/Users/mirror/phantomjs/bin/phantomjs')

    def getAllLinks(self, keyWord):
        allLinks = []
        pageNum = 0
        url = 'https://www.baidu.com/s?wd=site: amazon.ca ' + keyWord + ' currently unavailable&pn=' + str(
            pageNum * 10) + '&oq=site: amazon.ca headphones currently unavailable&ie=utf-8&usm=1'
        print(url)
        self.driver.get(url)
        page = self.driver.page_source
        isLastPage = self.isLastPage(page)
        detailLinks = self.getDetailLinks(page)
        allLinks = allLinks + detailLinks
        while not isLastPage:
            nextPageLinks2page = self.getNextPageLinks2page(keyWord, pageNum + 1)
            nextPageLinks = nextPageLinks2page[0]
            print(nextPageLinks)
            nextPage = nextPageLinks2page[1]
            isLastPage = self.isLastPage(nextPage)
            pageNum = pageNum + 1
            allLinks = allLinks + nextPageLinks
        return allLinks

    def isLastPage(self, page):
        if 'class="n">下一页' in page:
            return False
        else:
            return True

    def getNextPageLinks2page(self, keyWord, pageNum):
        url = 'https://www.baidu.com/s?wd=site: amazon.ca ' + keyWord + ' currently unavailable&pn=' + str(
            pageNum * 10) + '&oq=site: amazon.ca headphones currently unavailable&ie=utf-8&usm=1'

        self.driver.get(url)
        page = self.driver.page_source
        detailLinks = self.getDetailLinks(page)
        return detailLinks, page

    def getDetailLinks(self, page):
        detailLinks = []
        detailSoup = BeautifulSoup(page, "html.parser")
        targetLinks = detailSoup.select('.c-container > h3 > a')
        for targetLink in targetLinks:
            link = targetLink['href']
            realLink = self.getRealUrl(link)
            if 'www.amazon.ca' not in realLink:
                continue
            detailLinks.append(realLink)
        print(detailLinks)
        return detailLinks

    def getRealUrl(self,url):
        response = requests.get(url)
        return response.url


if __name__ == '__main__':
    while True:
        detailLinkDao = DetailLinkDao()
        keyWordDao = KeywordDao()
        id2keyword = keyWordDao.popKeyWordForRedis()
        if id2keyword is None:
            print('关键词没了，睡眠3秒')
            continue
        else:
            id2keywordDic = eval(id2keyword)
            keyWord = id2keywordDic[1]
            keywordId = id2keywordDic[0]
            search = Search()
            allLinks = search.getAllLinks(keyWord)
            keywordId2link = list()
            print('keyworId:'+str(keywordId))
            print('allLinks:'+str(allLinks))
            for link in allLinks:
                keywordId2link.append((link,keywordId))
            # 把详细页图片插入到数据库
            print('keywordId2link:'+str(keywordId2link))
            detailLinkDao.batchInsert(keywordId2link)
            keyWordDao.updateKeywordState(keywordId, 2)
            print(allLinks)
            print(len(allLinks))
        keyWordDao.close()
        detailLinkDao.close()
