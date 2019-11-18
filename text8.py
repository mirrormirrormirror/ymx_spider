#coding=utf8
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import requests

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('window-size=1920x3000')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)


def isIntercept(text):
    if 'Enter the characters you see below' in text:
        return True
    else:
        return False

count = 0

try:
    while True:
        driver.get('https://www.amazon.ca/dp/B07FP5PQYZ/rch')
        text = driver.page_source

        print(isIntercept(text))
        if count == 1000:
            break
    driver.close()
except:
    print("err")
    driver.close()


def parseReviews(text):
    reviewsPattern = 'a-size-base">\d+ ratings'
    reviewsStr = re.search(reviewsPattern, text)
    if reviewsStr is None:
        print('review skip')
    else:
        reviews = re.search(r'\d+', reviewsStr.group())
        return reviews.group()


def parseStars(text):
    startSoup = BeautifulSoup(text)
    text = str(startSoup.select('#acrPopover'))
    startsPattern = 'a-icon-alt">(.*?)</span></i>'
    startsStr = re.search(startsPattern, text).group()
    startsBefore = startsStr.split('a-icon-alt">')[1].split(' out of ')[0]
    starts = startsBefore
    return starts



def parseBrand(text):
    brandPattern = '<a id="bylineInfo" class="a-link-normal" href(.*?)</a>'
    brandStrGroup = re.search(brandPattern, text)
    if brandStrGroup is None:
        return 'NULL'
    else:
        brandStr = brandStrGroup.group()
        brand = brandStr.split('">')[1].split('</')[0]
        return brand


def parseAsin(text):
    asinPattern = 'name="ASIN" value="\w+"'
    asinStr = re.search(asinPattern, text).group()
    asinStr = asinStr.split('value="')[1]
    asinStr = asinStr.replace('"', '')
    return asinStr


def getCommentList(asin):
    postUrl = 'https://www.amazon.com/hz/reviews-render/ajax/medley-filtered-reviews/get/ref=cm_cr_dp_d_fltrs_srt'
    postPara = {'asin': asin, 'sortBy': 'recent', 'scope': 'reviewsAjax2'}

    commentList = requests.post(postUrl, data=postPara, timeout=5)
    return commentList.text


def parseLastReviewTime(text):
    lastReviewTimeStr = text.split("&&&")[2]
    lastReviewTimeStrGroup = re.search(r'secondary review-date\\">(.*?)</span>', lastReviewTimeStr)
    if lastReviewTimeStrGroup is None:
        return 'January 01, 2050'
    else:
        lastReviewTimeStr = lastReviewTimeStrGroup.group()
        lastReviewTimeResult = lastReviewTimeStr.split('>')[1].split('<')[0]
        return lastReviewTimeResult


def parseIsVariant(text):
    if '"format-strip-linkless' in text:
        return '1'
    else:
        return '0'


#
# # import requests
# # # proxies = { "http": "http://58.20.37.25:8181", "https": "58.20.37.25:8181" }
# # session = requests.session()
# # headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Referer': "www.google.com" }
# # page = session.get('https://www.amazon.com', headers=headers)
# # print(page.text)
# # page = requests.get("https://www.amazon.com/Bluetooth-Headphones-Wireless-Microphone-Cancelling/dp/B07CNCDSVM")
# # print(page.text)
#
#
# # import requests
# #
# # headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Referer': "www.google.com" }
# # session = requests.session()
# # session.get('https://www.amazon.com', headers=headers)
# # page = session.get('https://www.amazon.com/Bluetooth-Headphones-Wireless-Microphone-Cancelling/dp/B07CNCDSVM')
# # print(page.text)
# # session.close()
#
#
#
#
# import requests
# import time
#
#
# class TestCrawler:
#     def __init__(self):
#         # 要访问的目标页面
#         self.targetUrl = "https://www.amazon.ca/dp/B07FP5PQYZ/rch"
#         # 代理服务器
#         proxyHost = "http-dyn.abuyun.com"
#         proxyPort = "9020"
#
#         # 代理隧道验证信息
#         proxyUser = "HP5NM0H43UO0EMLD"
#         proxyPass = "20D6132CF6AD2266"
#
#         proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#             "host": proxyHost,
#             "port": proxyPort,
#             "user": proxyUser,
#             "pass": proxyPass,
#         }
#
#         self.proxies = {
#             "http": proxyMeta,
#             "https": proxyMeta,
#         }
#
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
#             'Referer': "www.google.com"}
#         self.session = requests.session()
#         iniResponse = self.session.get('https://www.amazon.ca', headers=self.headers,proxies=self.proxies)
#         print(iniResponse.status_code)
#         self.count = 0
#         self.countPoint = 0
#
#     def get(self):
#         while True:
#             response = self.session.get(self.targetUrl)
#             print(response.status_code)
#             self.count = self.count + 1
#             if self.count - self.countPoint > 2:
#                 self.countPoint = self.count
#                 self.session.close()
#                 self.session = self.newSession()
#             # time.sleep(1)
#
#     def newSession(self):
#         print('newSession')
#         newSession = requests.session()
#         newSession.get('https://www.amazon.ca', headers=self.headers,proxies=self.proxies)
#         return newSession
# if __name__ == '__main__':
#     testCrawler = TestCrawler()
#     testCrawler.get()

#
# # 要访问的目标页面
# targetUrl = "https://www.amazon.com/Dog-Seat-Cover-Protecting-Comfortable/dp/B01HDQCU74"
# # targetUrl = "http://proxy.abuyun.com/switch-ip"
# # targetUrl = "http://proxy.abuyun.com/current-ip"
#
# # 代理服务器
# proxyHost = "http-dyn.abuyun.com"
# proxyPort = "9020"
#
# # 代理隧道验证信息
# proxyUser = "HP5NM0H43UO0EMLD"
# proxyPass = "20D6132CF6AD2266"
#
# proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#     "host": proxyHost,
#     "port": proxyPort,
#     "user": proxyUser,
#     "pass": proxyPass,
# }
#
# proxies = {
#     "http": proxyMeta,
#     "https": proxyMeta,
# }
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
#     'Referer': "www.google.com"}
# session = requests.session()
#
# response = session.get('https://www.amazon.cn/b?node=1841388071&tag=baiduiclickcn-23&ref=AGS_1738_zhj_41180',
#                        headers=headers)
# print(response.status_code)
#
# while True:
#     resp = session.get(targetUrl)
#     print(resp.status_code)
#     # print(resp.text )
