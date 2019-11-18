import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import pymysql
import redis
from KeywordDao import KeywordDao
from DirDetailLinkDao import  DirDetailLinkDao

class DetailLinkDao:

    def __init__(self):
        self.db = pymysql.connect(host='cdb-8z1kodpo.bj.tencentcdb.com', port=10050, user='root', password='mirror123',
                                  database='ymx')
        self.cursor = self.db.cursor()

        self.myRedis = redis.Redis(host='localhost', port=6379, db=0)
        self.limit = 10
        self.seedDetailLink = 'seed_detail_link'
        self.duplicateLink = 'duplicate_link'

    def getKeyWordIdById(self, detailLinkId):
        getKeyWordIdByIdSql = 'select keyword_id from t_ymx_detail_link where id = %s'
        self.cursor.execute(getKeyWordIdByIdSql % detailLinkId)
        data = self.cursor.fetchall()
        if len(data) == 0:
            return None
        else:
            return data[0][0]

    def getKeyword2keywordIdByDetailLinkId(self, detailLinkId):
        keywordId = self.getKeyWordIdById(detailLinkId)
        dirDetailLinkDao = DirDetailLinkDao()

        if keywordId is None:
            keywordId = dirDetailLinkDao.getKeyWordIdById(detailLinkId)
            dirDetailLinkDao.close()

        keywordDao = KeywordDao()
        keyword = keywordDao.getKeywordById(keywordId)
        keywordDao.close()
        return keyword,keywordId

    def batchInsert(self, keywordId2detailLink):
        print('keywordId2detailLink:'+str(keywordId2detailLink))
        batchInsertDetailLinkSql = 'INSERT INTO `t_ymx_detail_link` ( `detail_link`,  `keyword_id`) VALUES'
        for row in keywordId2detailLink:
            batchInsertDetailLinkSql = batchInsertDetailLinkSql + ' ("%s",%s)' % (row[0], row[1]) + ','
        batchInsertDetailLinkSql = batchInsertDetailLinkSql[0:len(batchInsertDetailLinkSql) - 1]
        print(batchInsertDetailLinkSql)
        self.cursor.execute(batchInsertDetailLinkSql)
        self.db.commit()

    def putDetailLinksToRedis(self):
        ids = '-1'
        batchUpdateDetailLinkJobStateSql = 'update t_ymx_detail_link set job_state=1 where id in (%s)'
        id2detailLink = self.getId2detailLink()
        for detailLinkId, detailLink in zip(id2detailLink.keys(), id2detailLink.values()):
            ids = ids + ',' + str(detailLinkId)
            self.myRedis.sadd(self.seedDetailLink, str((detailLinkId, detailLink)))

        print(batchUpdateDetailLinkJobStateSql % ids)
        self.cursor.execute(batchUpdateDetailLinkJobStateSql % ids)
        self.db.commit()

    def isLowLevelDetailLinksForRedis(self):
        seedDetailLinkLen = self.myRedis.scard(self.seedDetailLink)
        print('详细页连接数：' + str(seedDetailLinkLen))
        if seedDetailLinkLen < self.limit:
            return True
        else:
            return False

    def getId2detailLink(self):
        id2detailLink = {}
        selectId2detailLinkSql = 'select id,detail_link from t_ymx_detail_link where job_state=0 order by id limit %s'
        self.cursor.execute(selectId2detailLinkSql % self.limit)
        data = self.cursor.fetchall()
        for row in data:
            id2detailLink[row[0]] = row[1]
        return id2detailLink

    def updateJobStateById(self, jobState, detailLinkId):
        updateJobStateByIdSql = 'update t_ymx_detail_link set job_state=%s where id = %s' % (jobState, detailLinkId)
        self.cursor.execute(updateJobStateByIdSql)
        self.db.commit()

    def popId2detailLinkForRedis(self):
        id2detailLinkForRedis = self.myRedis.spop(self.seedDetailLink)
        if id2detailLinkForRedis is None:
            return None
        else:
            return id2detailLinkForRedis.decode('utf-8')

    def close(self):
        self.db.close()
        self.myRedis.close()


if __name__ == '__main__':
    detailLinkDao = DetailLinkDao()
    # detailLinkDao.batchInsert({2: 'key1', 3: 'key2'})
    # isLowLevelDetailLinksForRedis = detailLinkDao.isLowLevelDetailLinksForRedis()
    # print(isLowLevelDetailLinksForRedis)
    # detailLinkDao.updateJobStateById(8, 5)

    keywordId = detailLinkDao.getKeyWordIdById(3)
    detailLinkDao.close()
    print(keywordId)
