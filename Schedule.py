
from DetailLinkDao import DetailLinkDao
from KeywordDao import KeywordDao
from DirDetailLinkDao import DirDetailLinkDao
import time
from SlpLinkDao import SlpLinkDao

if __name__ == '__main__':
    while True:
        keywordDao = KeywordDao()

        print("into keyword logic")
        isLowLevelKeywordForRids = keywordDao.isLowLevelKeywordForRids()
        if isLowLevelKeywordForRids:
            print('redis seed_keyword  low put mysql data to redis..')
            keywordDao.putKeywordToRedis()
        else:
            print('redis seed_keyword normal')

        keywordDao.close()

        detailLinkDao = DetailLinkDao()
        isLowLevelDetailLinksForRedis = detailLinkDao.isLowLevelDetailLinksForRedis()
        if isLowLevelDetailLinksForRedis:
            print('redis seed_detail_link low put mysql data to redis..')
            detailLinkDao.putDetailLinksToRedis()
        else:
            print('redis seed_detail_link normal')
        detailLinkDao.close()

        dirDetailLinkDao = DirDetailLinkDao()
        if dirDetailLinkDao.isLowLevelDetailLinksForRedis():
            print('redis seed_dir_detail_link low put mysql data to redis..')
            dirDetailLinkDao.putDetailLinksToRedis()
        else:
            print('redis seed_dir_detail_link normal')
        dirDetailLinkDao.close()


        slpLinkDao = SlpLinkDao()
        isLowLevelDetailLinksForRedis = slpLinkDao.isLowLevelDetailLinksForRedis()
        if isLowLevelDetailLinksForRedis:
            print('low slp')
            slpLinkDao.putSlpLinksToRedis()
        slpLinkDao.close()
        time.sleep(3)
