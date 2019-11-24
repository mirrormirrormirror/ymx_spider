import requests
import re
from DetailLinkDao import DetailLinkDao
from DetailDao import DetailDao
from bs4 import BeautifulSoup
import time
from DirDetailLinkDao import DirDetailLinkDao
from chrome import Chrome
from Download import Download
from SlpLinkDao import SlpLinkDao


class Detail:
    def __init__(self):
        self.chrome = Chrome()
        # self.download = Download()

    def parseReviews(self, text):
        reviewsPattern = 'a-size-base">\d+ ratings'
        reviewsStr = re.search(reviewsPattern, text)
        if reviewsStr is None:
            print('page abnormal skip')
        else:
            reviews = re.search(r'\d+', reviewsStr.group())
            return reviews.group()

    def parseAsin(self, text):
        asinPattern = 'name="ASIN" value="\w+"'
        asinStr = re.search(asinPattern, text).group()
        asinStr = asinStr.split('value="')[1]
        asinStr = asinStr.replace('"', '')
        return asinStr

    def parseStars(self, text):
        startSoup = BeautifulSoup(text)
        text = str(startSoup.select('#acrPopover'))
        startsPattern = 'a-icon-alt">(.*?)</span></i>'
        startsStr = re.search(startsPattern, text).group()
        startsBefore = startsStr.split('a-icon-alt">')[1].split(' out of ')[0]
        starts = startsBefore
        return starts

    def parseBrand(self, text):
        brandPattern = '<a id="bylineInfo" class="a-link-normal" href(.*?)</a>'
        brandStrGroup = re.search(brandPattern, text)
        if brandStrGroup is None:
            return 'NULL'
        else:
            brandStr = brandStrGroup.group()
            brand = brandStr.split('">')[1].split('</')[0]
            return brand

    def parseLastReviewTime(self, text):
        lastReviewTimeStr = text.split("&&&")[2]
        lastReviewTimeStrGroup = re.search(r'secondary review-date\\">(.*?)</span>', lastReviewTimeStr)
        if lastReviewTimeStrGroup is None:
            print(lastReviewTimeStr)
            return 'January 01, 2020'
        else:
            lastReviewTimeStr = lastReviewTimeStrGroup.group()
            lastReviewTimeResult = lastReviewTimeStr.split('>')[1].split('<')[0]
            return lastReviewTimeResult

    def parseIsVariant(self, text):
        if '"format-strip-linkless' in text:
            return '1'
        else:
            return '0'

    def getCommentList(self, asin):
        postUrl = 'https://www.amazon.ca/hz/reviews-render/ajax/medley-filtered-reviews/get/ref=cm_cr_dp_d_fltrs_srt'
        # getUrl = 'https://www.amazon.ca/hz/reviews-render/ajax/medley-filtered-reviews/get/ref=cm_cr_dp_d_fltrs_srt'
        postPara = {'asin': asin, 'sortBy': 'helpful', 'scope': 'reviewsAjax2'}

        commentList = requests.post(postUrl, data=postPara, timeout=5)
        return commentList.text

    def parseTitle(self, page):
        detailSoup = BeautifulSoup(page, "html.parser")
        title = detailSoup.title.string.strip()
        title.replace('"', "'")
        return title

    def crawl(self, url, detailLinkId):
        # page = self.download.download(url)
        page = self.chrome.download(url)

        if self.isDirPage(page):
            print('is dir ,need to parse detail link')
            detailLinkDao = DetailLinkDao()
            dirDetailLinkDao = DirDetailLinkDao()
            keywordId2link = []
            dirDetailLinks = self.parseDirDetailLinks(page)
            dirDetailLinksSet = set(dirDetailLinks)
            print(len(dirDetailLinksSet))
            for link in dirDetailLinksSet:
                keywordId = detailLinkDao.getKeyWordIdById(detailLinkId)
                keywordId2link.append((link, keywordId))

            dirDetailLinkDao.batchInsert(keywordId2link)
            detailLinkDao.close()
            dirDetailLinkDao.close()

        else:
            detailLinkDao = DetailLinkDao()
            if 'www.amazon.ca' not in page:
                print('not www.amazon.ca skip')
                detailLinkDao.updateJobStateById(-1, detailLinkId)
                return None
            elif self.isIntercept(page):
                print('isIntercept skip')
                detailLinkDao.updateJobStateById(3, detailLinkId)
                time.sleep(10)
                return None
            elif self.isUnavailable(page):
                print('not Unavailable')
                detailLinkDao.updateJobStateById(3, detailLinkId)

            reviews = self.parseReviews(page)
            if reviews is None:
                print('page abnormal skip')
                detailLinkDao.updateJobStateById(3, detailLinkId)
                return None
            detailLinkDao.close()
            asin = self.parseAsin(page)

            stars = self.parseStars(page)

            brand = self.parseBrand(page)
            try:
                commentList = self.getCommentList(asin)
                lastReviewTime = self.parseLastReviewTime(commentList)
                isVariant = self.parseIsVariant(commentList)
            except Exception as e:
                print(e)
                lastReviewTime = 'January 01, 2030'
                isVariant = '1'

            if lastReviewTime == 'NULL':
                lastReviewTimeFormat = lastReviewTime
            else:
                lastReviewTimeFormat = self.formatTime(lastReviewTime)
            title = self.parseTitle(page)
            row = {'asin': asin, 'stars': stars, 'brand': brand, 'lastReviewTime': lastReviewTimeFormat,
                   'isVariant': isVariant,
                   'reviews': reviews, 'title': title}
            rowOther = {'asin': asin, 'stars': stars, 'brand': brand, 'lastReviewTime': lastReviewTimeFormat,
                   'isVariant': isVariant,
                   'reviews': reviews, 'title': 'title'}

            print(rowOther)
            return row

    def formatTime(self, dateStr):
        print(dateStr)
        dateStr = dateStr.replace(',', '')
        if 'January' in dateStr:
            dateStr = dateStr.replace('January', '01')
        elif 'February' in dateStr:
            dateStr = dateStr.replace('February', '02')
        elif 'March' in dateStr:
            dateStr = dateStr.replace('March', '03')
        elif 'April' in dateStr:
            dateStr = dateStr.replace('April', '04')
        elif 'May' in dateStr:
            dateStr = dateStr.replace('May', '05')
        elif 'June' in dateStr:
            dateStr = dateStr.replace('June', '06')
        elif 'July' in dateStr:
            dateStr = dateStr.replace('July', '07')
        elif 'August' in dateStr:
            dateStr = dateStr.replace('August', '08')
        elif 'September' in dateStr:
            dateStr = dateStr.replace('September', '09')
        elif 'October' in dateStr:
            dateStr = dateStr.replace('October', '10')
        elif 'November' in dateStr:
            dateStr = dateStr.replace('November', '11')
        elif 'December' in dateStr:
            dateStr = dateStr.replace('December', '12')
        dateStrList = dateStr.split(' ')
        return dateStrList[2] + '-' + dateStrList[0] + '-' + dateStrList[1] + ' 00:00:00'

    def isIntercept(self, text):
        if 'Enter the characters you see below' in text:
            return True
        else:
            return False


    def isUnavailable(self, text):
        if 'Currently unavailable' in text:
            return True
        else:
            return False

    def parseDirDetailLinks(self, text):
        links = []
        soup = BeautifulSoup(text)
        container = soup.select('.FS-CLP-desktop-page-container')[0]
        linksSoup = container.select('.a-fixed-left-grid-col')
        for linkSoup in linksSoup:
            hrefSoup = linkSoup.select('.a-link-normal')
            if 'a-link-normal' in str(hrefSoup):
                href = hrefSoup[0]['href']
                href = 'https://www.amazon.com' + href
                links.append(href)
        return links

    def isDirPage(self, text):
        if 'FS-CLP-desktop-page-container' in text:
            return True
        else:
            return False

    def close(self):
        # self.download.close()
        self.chrome.close()


    def run(self):
        while True:
            detailLinkDao = DetailLinkDao()
            # 从redis中获取url
            id2detailLink = detailLinkDao.popId2detailLinkForRedis()
            if id2detailLink is None:
                print('not link stop 3 second')
                time.sleep(3)
                continue

            id2detailLinkDic = eval(id2detailLink)
            print('id2detailLinkDic:' + str(id2detailLinkDic))
            detailLinkId = id2detailLinkDic[0]
            detailLink = id2detailLinkDic[1]

            if '/dp/' not in detailLink:
                continue
            detailData = self.crawl(detailLink, detailLinkId)
            if detailData is None:
                print('fail:' + id2detailLink)
                continue

            detailDao = DetailDao()
            keyword2keywordId = detailLinkDao.getKeyword2keywordIdByDetailLinkId(detailLinkId)

            detailDao.insert(detailData['asin'], float(detailData['stars']), int(detailData['reviews']),
                             detailData['lastReviewTime'], detailData['title'], detailData['brand'],
                             keyword2keywordId[0],
                             keyword2keywordId[1], detailLink, detailLinkId,
                             int(detailData['isVariant']))
            detailLinkDao.updateJobStateById(2, detailLinkId)
            detailLinkDao.close()
            time.sleep(1)


if __name__ == '__main__':
    while True:
        try:
            detail = Detail()
            detail.run()

        except:
            print('detail fail:')
        finally:
            detail.close()
            time.sleep(2)

    # dateStr = 'April 5, 2019'
    # url = 'http://www.baidu.com/link?url=W030YCfQnj265IjnUV5UGGYPxT2TVAX5zGsKzVSXw9A_afUXjv0GiqnVmpDQJHu3JyutO7nV2pnzn-F8S-p_FPBS97P7eGMSx__cDOTUJwHLvotAbEM8p_4uoNYF7e9uaGWS2sC1N04HEJ0Yzd5pqa'
    # detail = Detail()
    # # time  = detail.formatTime(dateStr)
    # print(time)
    # detail.run(url, 2)
