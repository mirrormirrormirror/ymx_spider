from selenium import webdriver
import time
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
# chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
# chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
# chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
# chrome_options.add_argument('--headless')

driver = webdriver.Chrome()

driver.get('https://cn.bing.com/?scope=web&FORM=QBRE')
driver.find_element_by_css_selector('#sb_form_q').send_keys('site: amazon.com headphones currently unavailable')
driver.find_element_by_css_selector('#sb_form_go').click()
time.sleep(200)
print(driver.page_source)
driver.close()
