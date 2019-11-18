#coding=utf8
from DetailLinkDao import DetailLinkDao
from KeywordDao import KeywordDao
from DirDetailLinkDao import DirDetailLinkDao
import time

if __name__ == '__main__':
    while True:
        keywordDao = KeywordDao()

        print(u"进入关键词调度逻辑------")
        isLowLevelKeywordForRids = keywordDao.isLowLevelKeywordForRids()
        if isLowLevelKeywordForRids:
            print(u'redis中的seed_keyword关键词个数低于阈值！put mysql data to redis..')
            keywordDao.putKeywordToRedis()
        else:
            print(u'redis中的seed_keyword关键词个数正常')

        keywordDao.close()

        detailLinkDao = DetailLinkDao()
        isLowLevelDetailLinksForRedis = detailLinkDao.isLowLevelDetailLinksForRedis()
        if isLowLevelDetailLinksForRedis:
            print(u'redis中的seed_detail_link连接个数低于阈值！put mysql data to redis..')
            detailLinkDao.putDetailLinksToRedis()
        else:
            print(u'redis中的seed_detail_link连接个数正常')
        detailLinkDao.close()

        dirDetailLinkDao = DirDetailLinkDao()
        if dirDetailLinkDao.isLowLevelDetailLinksForRedis():
            print(u'redis中的seed_dir_detail_link连接个数低于阈值！put mysql data to redis..')
            dirDetailLinkDao.putDetailLinksToRedis()
        else:
            print(u'redis中的seed_dir_detail_link连接个数正常')

        time.sleep(5)
