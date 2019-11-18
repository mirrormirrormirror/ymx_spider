#coding=utf8
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import requests


class Download:
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Referer': "www.google.com"}
        self.session = requests.session()
        self.session.get('https://www.amazon.com',headers = headers)

    def download(self, url):
        page = self.session.get(url)
        print(page.status_code)
        return page.text

    def close(self):
        self.session.close()


if __name__ == '__main__':
    download = Download()
    download.download(
        'http://www.baidu.com/link?url=FjhiqWdQzaWpdlVbHzvU7i4z_EoXfCwhRQbC69Lg4aIoh-9t72rFUQVDmdXzIbD93wp8MtONJnpHUhsp88FTJNu5W3_l4WdBk8HLOfuQuiFAes5aCI2QPxuMsHtphUcM')
    download.close()
