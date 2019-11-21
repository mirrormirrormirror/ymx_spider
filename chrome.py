from selenium import webdriver
from selenium.common.exceptions import TimeoutException


class Chrome:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('window-size=1920x3000')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--proxy-server=%s' % 'http://198.211.117.191:3128')
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.set_page_load_timeout(10)
        self.driver.get('https://www.amazon.ca')

    def download(self, url):
        try:
            try:
                print('download')
                self.driver.get(url)
                print('download finish')
                page = self.driver.page_source
                print('page_source finish')
            except TimeoutException:
                print('time out')
                # 报错后就强制停止加载
                # 这里是js控制
                self.driver.close()
                self.__init__()
                self.driver.get(url)
                page = self.driver.page_source
        except:
            page = 'aaaa'
        return page

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    chrome = Chrome()
    text = chrome.download('https://www.amazon.com/dp/B00XNC2HEE?m=A3V5HUUW6T218W&ref_=v_sp_widget_detail_page')
    print(text)
