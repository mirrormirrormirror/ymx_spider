
from selenium import webdriver



class Chrome:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('window-size=1920x3000')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options = chrome_options)


    def download(self,url):
        print('download')
        self.driver.get(url)
        page = self.driver.page_source
        print('download finish')
        return page

    def close(self):
        self.driver.close()




if __name__ == '__main__':
    chrome = Chrome()
    text = chrome.download('https://www.amazon.com/dp/B00XNC2HEE?m=A3V5HUUW6T218W&ref_=v_sp_widget_detail_page')
    print(text)