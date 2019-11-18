
from selenium import webdriver



class Chrome:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
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