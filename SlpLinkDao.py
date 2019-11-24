import pymysql
import redis
from KeywordDao import KeywordDao
from DirDetailLinkDao import DirDetailLinkDao


class SlpLinkDao:

    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='mirror123', database='ymx')
        self.cursor = self.db.cursor()

        self.myRedis = redis.Redis(host='localhost', port=6379, db=0)
        self.limit = 10
        self.seedSlplLink = 'seed_slp_link'
        self.duplicateLink = 'duplicate_link'

    def getKeyWordIdById(self, detailLinkId):
        getKeyWordIdByIdSql = 'select keyword_id from t_ymx_slp_link where id = %s'
        self.cursor.execute(getKeyWordIdByIdSql % detailLinkId)
        data = self.cursor.fetchall()
        if len(data) == 0:
            return None
        else:
            return data[0][0]

    # def getKeyword2keywordIdBySlpLinkId(self, slpLinkId):
    #     keywordId = self.getKeyWordIdById(slpLinkId)
    #     dirDetailLinkDao = DirDetailLinkDao()
    #
    #     if keywordId is None:
    #         keywordId = dirDetailLinkDao.getKeyWordIdById(detailLinkId)
    #         dirDetailLinkDao.close()
    #
    #     keywordDao = KeywordDao()
    #     keyword = keywordDao.getKeywordById(keywordId)
    #     keywordDao.close()
    #     return keyword, keywordId

    def batchInsert(self, keywordId2slpLink):
        print('keywordId2slpLink:' + str(keywordId2slpLink))
        if len(keywordId2slpLink) == 0:
            return
        batchInsertDetailLinkSql = 'INSERT INTO `t_ymx_slp_link` ( `slp_link`,  `keyword_id`) VALUES'
        for row in keywordId2slpLink:
            batchInsertDetailLinkSql = batchInsertDetailLinkSql + ' ("%s",%s)' % (row[0], row[1]) + ','
        batchInsertDetailLinkSql = batchInsertDetailLinkSql[0:len(batchInsertDetailLinkSql) - 1]
        print(batchInsertDetailLinkSql)
        self.cursor.execute(batchInsertDetailLinkSql)
        self.db.commit()

    def putSlpLinksToRedis(self):
        ids = '-1'
        batchUpdateSlpLinkJobStateSql = 'update t_ymx_slp_link set job_state=1 where id in (%s)'
        id2slpLink = self.getId2slpLink()
        print('id2slpLink:' + str(id2slpLink))
        for slpLinkId, slpLink in zip(id2slpLink.keys(), id2slpLink.values()):
            ids = ids + ',' + str(slpLinkId)
            self.myRedis.sadd(self.seedSlplLink, str((slpLinkId, slpLink)))

        print(batchUpdateSlpLinkJobStateSql % ids)
        self.cursor.execute(batchUpdateSlpLinkJobStateSql % ids)
        self.db.commit()

    def isLowLevelDetailLinksForRedis(self):
        seedSlpLinkLen = self.myRedis.scard(self.seedSlplLink)
        print('slp page link len' + str(seedSlpLinkLen))
        if seedSlpLinkLen < self.limit:
            return True
        else:
            return False

    def getId2slpLink(self):
        id2slpLink = {}
        selectId2slpLinkSql = 'select id,slp_link from t_ymx_slp_link where job_state=0 order by id limit %s'
        print('selectId2detailLinkSql:' + selectId2slpLinkSql % self.limit)
        self.cursor.execute(selectId2slpLinkSql % self.limit)
        data = self.cursor.fetchall()
        for row in data:
            id2slpLink[row[0]] = row[1]
        return id2slpLink

    def updateJobStateById(self, jobState, slpLinkId):
        updateJobStateByIdSql = 'update t_ymx_slp_link set job_state=%s where id = %s' % (jobState, slpLinkId)
        print(updateJobStateByIdSql)
        self.cursor.execute(updateJobStateByIdSql)
        self.db.commit()

    def popId2slpLinkForRedis(self):
        id2slpLinkForRedis = self.myRedis.spop(self.seedSlplLink)
        if id2slpLinkForRedis is None:
            return None
        else:
            return id2slpLinkForRedis.decode('utf-8')

    def close(self):
        self.db.close()
        self.myRedis.close()


if __name__ == '__main__':
    pass