from src.KeywordDao import KeywordDao

if __name__ == '__main__':
    keywordDao = KeywordDao()
    keywords = list()
    f = open('keyword/keywor20190008.txt')
    keywords = f.readlines()

    for keyword in keywords:
        keyword = keyword.replace('\n', '')
        print(keyword)
        keywordDao.insert(keyword, 0)
    keywordDao.close()
