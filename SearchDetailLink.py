import requests
from DetailLinkDao import DetailLinkDao
from SlpLinkDao import SlpLinkDao
from KeywordDao import KeywordDao
import time
from bs4 import BeautifulSoup
import re


class SearchDetailLink:
    def __init__(self):
        self.session = requests.session()
        self.session.get('https://www.amazon.ca')

    def download(self, url):
        page = self.session.get(url)
        if page.status_code == 200:
            return page.text
        else:
            return None

    def run(self, url):
        text = self.download(url)
        if text is not None:
            detailLinks = self.parseDetailLink(text)
            print(detailLinks)
            return list(detailLinks)
        else:
            return []

    def parseDetailLink(self, text):
        result = set()
        allLinks = []
        soup = BeautifulSoup(text)
        detailListSop = soup.select('div.FS-CLP-desktop-page-container > .a-fixed-right-grid')
        # print(detailListSop)
        for detailSop in detailListSop:
            if 'Currently unavailable' in str(detailSop):
                links = re.findall('/dp/[a-zA-Z0-9-]+', str(detailSop))
                allLinks = allLinks + links

        for link in allLinks:
            result.add('https://www.amazon.ca' + link)
        return result

    def close(self):
        pass


if __name__ == '__main__':
    while True:
        searchDetailLink = SearchDetailLink()
        slpLinkDao = SlpLinkDao()
        detailLinkDao = DetailLinkDao()
        keywordDao = KeywordDao()
        try:
            id2slpLink = slpLinkDao.popId2slpLinkForRedis()
            print(id2slpLink)

            print(time.strftime(' %Y-%m-%d %H:%M:%S %p %w ', time.localtime(time.time())))
            if id2slpLink is None:
                print('no id2slpLink stop 3 second')
                time.sleep(3)
                continue
            else:
                print('go to run slp')
                id2slpDic = eval(id2slpLink)
                slpLink = id2slpDic[1]
                slpId = id2slpDic[0]
                detailLinks = searchDetailLink.run(slpLink)

                keywordId = slpLinkDao.getKeyWordIdById(slpId)
                keywordId2link = list()
                print('keyworId:' + str(keywordId))
                print('allLinks:' + str(detailLinks))
                for link in detailLinks:
                    keywordId2link.append((link, keywordId))
                # 把详细页图片插入到数据库
                print('keywordId2link:' + str(keywordId2link))
                if len(detailLinks) == 0:
                    print('no detail link----skip')
                    slpLinkDao.updateJobStateById(slpId, 2)
                    continue

                detailLinkDao.batchInsert(keywordId2link)
                slpLinkDao.updateJobStateById(2, slpId)

        except Exception as e:
            print(e)
        finally:
            print('finally')
            searchDetailLink.close()
            slpLinkDao.close()
            detailLinkDao.close()
            keywordDao.close()
            time.sleep(3)

# searchDetailLink = SearchDetailLink()
# a = searchDetailLink.run('https://www.amazon.ca/slp/2qxeg8avtgsf67y')
# print(a)
