
import requests


class Download:
    def __init__(self):
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        #     'Referer': "www.google.com"}
        self.session = requests.session()
        self.session.get('https://www.amazon.ca')

    def download(self, url):
        page = self.session.get(url)
        print(page.status_code)
        return page.text

    def close(self):
        self.session.close()


if __name__ == '__main__':
    download = Download()
    download.download('https://www.amazon.ca/dp/B07FLHJNQ1')
    download.close()
