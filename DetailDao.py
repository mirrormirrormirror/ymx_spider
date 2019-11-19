import pymysql


class DetailDao:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='mirror123', database='ymx')
        self.cursor = self.db.cursor()

    def insert(self, asin, stars, reviews, last_review_time, title, brand, keyword, keyword_id, detail_link,
               detail_link_id, is_variant):
        insertSql = 'INSERT INTO `t_ymx_detail` ( `asin`, `stars`, `reviews`, `last_review_time`, `title`, `brand`, `keyword`, `keyword_id`,`detail_link`, `detail_link_id`, `is_variant`) VALUES ("%s",%s,%s,"%s","%s","%s","%s",%s,"%s",%s,%s) '
        print(insertSql % (
            asin, stars, reviews, last_review_time, pymysql.escape_string(title.encode('utf-8')), brand, keyword, keyword_id,
            detail_link, detail_link_id, is_variant))
        self.cursor.execute(insertSql % (
            asin, stars, reviews, last_review_time, pymysql.escape_string(title.encode('utf-8')), brand, keyword, keyword_id,
            detail_link, detail_link_id, is_variant))
        self.db.commit()

    def close(self):
        self.db.close()


if __name__ == '__main__':
    detailDao = DetailDao()
    detailDao.insert('B076TZ8HD3', 3.8, 59, '2019-11-14 20:42:57', 'title', 'TRANYA', 'keyword', 2,
                     'https://www.amazon.com/Wireless-Headphones-Bluetooth-Earphones-Microphone/dp/B076TZ8HD3', 2, 0)
