import pymysql
import redis


class KeywordDao:

    def __init__(self):
        self.db = pymysql.connect(host='cdb-8z1kodpo.bj.tencentcdb.com', port=10050, user='root', password='mirror123',
                                  database='ymx')
        self.cursor = self.db.cursor()

        self.myRedis = redis.Redis(host='localhost', port=6379, db=0)

        self.seedKeyword = 'seed_keyword'
        self.limit = 10

    def popKeyWordForRedis(self):
        id2keyword = self.myRedis.spop(self.seedKeyword)
        if id2keyword is None:
            return None
        else:
            return id2keyword.decode('utf-8')

    # 把关键词放到redis上
    def putKeywordToRedis(self):
        ids = '-1'
        batchUpdateKeywordJobStateSql = 'update t_ymx_keyword set job_state=1 where id in (%s)'
        id2keyword = self.getId2keyword()
        for keywordId, keyword in zip(id2keyword.keys(), id2keyword.values()):
            ids = ids + ',' + str(keywordId)
            self.myRedis.sadd(self.seedKeyword, str((keywordId, keyword)))
        print(batchUpdateKeywordJobStateSql % ids)
        self.cursor.execute(batchUpdateKeywordJobStateSql % ids)
        self.db.commit()

    # 判断redis上的关键词是不是低于limit个
    def isLowLevelKeywordForRids(self):
        seedKeywordLen = self.myRedis.scard(self.seedKeyword)
        print('关键词个数为：' + str(seedKeywordLen))
        if seedKeywordLen < self.limit:
            return True
        else:
            return False

    # 更新keyword的state
    def updateKeywordState(self, keywordId, jobState):
        updateKeywordStateSql = 'update t_ymx_keyword set job_state=%s where id = %s'
        self.cursor.execute(updateKeywordStateSql % (jobState, keywordId))
        self.db.commit()

    def getId2keyword(self):
        id2keyword = {}
        selectKeyWordSql = 'select id,keyword from t_ymx_keyword where job_state=0 order by id limit %s'
        self.cursor.execute(selectKeyWordSql % self.limit)
        data = self.cursor.fetchall()
        for row in data:
            id2keyword[row[0]] = row[1]
        return id2keyword

    def getKeywordById(self, keywordId):
        getKeywordById = 'select keyword from t_ymx_keyword where id = %s'
        self.cursor.execute(getKeywordById % keywordId)
        data = self.cursor.fetchall()
        return data[0][0]

    def popId2keyword(self):
        id2keyword = self.myRedis.spop(self.seedKeyword)
        return id2keyword.decode('utf-8')

    def insert(self, keyword, jobState):
        insertSql = 'INSERT INTO `t_ymx_keyword` ( `keyword`, `job_state`) VALUES ("%s", %s);'
        self.cursor.execute(insertSql % (keyword, jobState))
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.myRedis.close()


if __name__ == '__main__':
    keywordDao = KeywordDao()
    # id2keyword = keywordDao.getId2keyword()
    # print(id2keyword)

    # keywordDao.putKeywordToRedis()

    # isLowLevelKeywordForRids = keywordDao.isLowLevelKeywordForRids()
    # print(isLowLevelKeywordForRids)

    # keywordDao.updateKeywordState(20,3)
    id2keyword = keywordDao.popId2keyword()
    print(id2keyword.decode('utf-8'))
    keywordDao.close()
