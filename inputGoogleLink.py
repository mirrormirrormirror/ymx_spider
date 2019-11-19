
import pymysql
if __name__ == '__main__':
    db = pymysql.connect(host='localhost', user='root', password='aa123', database='ymx')
    cursor = db.cursor()
    f = open('keyword/keywor20190008.txt')
    keywords = f.readlines()
    insertSql = 'INSERT INTO `t_ymx_google_host` ( `google_host`) VALUES("%s");'

    for keyword in keywords:
        keyword = keyword.replace('\n', '')
        cursor.execute(insertSql % keyword)
        db.commit()
    db.close()


