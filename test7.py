from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.amazon.com/errors/validateCaptcha?amzn=V48AfhoRuubyLhIv%2BpyQfQ%3D%3D&amzn-r=%2Fdp%2FB07FSQPT54&field-keywords=tmxxan')
isOk = input("is ok?")
if 'ok' == isOk:
    driver.get('https://www.amazon.com/Creuset-PG1854-1367-Stoneware-Heritage-Dishes/dp/B00ECS266C?ref_=fsclp_pl_dp_2')
    page = driver.page_source
    print(page)
    driver.get('https://www.amazon.com/JynXos-Ceramic-Pastoral-Bathroom-Accessories/dp/B06X986H9K?ref_=fsclp_pl_dp_14')
    page = driver.page_source
    print(page)
    driver.get('https://www.amazon.com/ScandinavianShoppe-218-51-Swedish-Dishcloth-Cherries/dp/B00IM0134W?ref_=fsclp_pl_dp_8')
    page = driver.page_source
    print(page)
driver.close()