import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import pymysql
import redis


class DirDetailLinkDao:
    def __init__(self):
        self.db = pymysql.connect(host='cdb-8z1kodpo.bj.tencentcdb.com', port=10050, user='root', password='mirror123',
                                  database='ymx')
        self.cursor = self.db.cursor()

        self.myRedis = redis.Redis(host='localhost', port=6379, db=0)
        self.limit = 10
        self.seedDirDetailLink = 'seed_dir_detail_link'
        self.duplicateLink = 'duplicate_link'

    def batchInsert(self, keywordId2detailLink):
        print('keywordId2detailLink:'+str(keywordId2detailLink))
        batchInsertDetailLinkSql = 'INSERT INTO `t_ymx_dir_detail_link` ( `detail_link`,  `keyword_id`) VALUES'
        for row in keywordId2detailLink:
            batchInsertDetailLinkSql = batchInsertDetailLinkSql + ' ("%s",%s)' % (row[0], row[1]) + ','
        batchInsertDetailLinkSql = batchInsertDetailLinkSql[0:len(batchInsertDetailLinkSql) - 1]
        print(batchInsertDetailLinkSql)
        self.cursor.execute(batchInsertDetailLinkSql)
        self.db.commit()

    def getId2detailLink(self):
        id2detailLink = {}
        selectId2detailLinkSql = 'select id,detail_link from t_ymx_dir_detail_link where job_state=0 order by id limit %s'
        self.cursor.execute(selectId2detailLinkSql % self.limit)
        data = self.cursor.fetchall()
        for row in data:
            id2detailLink[row[0]] = row[1]
        return id2detailLink

    def isLowLevelDetailLinksForRedis(self):
        seedDetailLinkLen = self.myRedis.scard(self.seedDirDetailLink)
        print('详细页连接数：' + str(seedDetailLinkLen))
        if seedDetailLinkLen < self.limit:
            return True
        else:
            return False
    def getKeyWordIdById(self, detailLinkId):
        getKeyWordIdByIdSql = 'select keyword_id from t_ymx_dir_detail_link where id = %s'
        self.cursor.execute(getKeyWordIdByIdSql % detailLinkId)
        data = self.cursor.fetchall()
        if len(data) == 0:
            return None
        else:
            return data[0][0]

    def popId2detailLinkForRedis(self):
        id2detailLinkForRedis = self.myRedis.spop(self.seedDirDetailLink)
        if id2detailLinkForRedis is None:
            return None
        else:
            return id2detailLinkForRedis.decode('utf-8')

    def putDetailLinksToRedis(self):
        ids = '-1'
        batchUpdateDetailLinkJobStateSql = 'update t_ymx_dir_detail_link set job_state=1 where id in (%s)'
        id2detailLink = self.getId2detailLink()
        for detailLinkId, detailLink in zip(id2detailLink.keys(), id2detailLink.values()):
            ids = ids + ',' + str(detailLinkId)
            self.myRedis.sadd(self.seedDirDetailLink, str((detailLinkId, detailLink)))

        print(batchUpdateDetailLinkJobStateSql % ids)
        self.cursor.execute(batchUpdateDetailLinkJobStateSql % ids)
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.myRedis.close()

