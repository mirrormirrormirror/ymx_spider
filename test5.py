from selenium import webdriver

options = webdriver.ChromeOptions()

proxyHost = "171.35.168.132"
proxyPort = "9999"

proxyMeta = "http://%(host)s:%(port)s" % {

    "host": proxyHost,
    "port": proxyPort,
}
proxies = {
    "http": proxyMeta,
}

# 设置语言
options.add_argument('lang=zh_CN.UTF-8')

# 不显示界面
options.add_argument('headless')

# 设置user-agent请求头
options.add_argument('user-agent=%s' % 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')

# 设置代理
options.add_argument('--proxy-server=%s' % proxies)
# http://127.0.0.1

# 图片不加载
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}
options.add_experimental_option('prefs', prefs)

browser = webdriver.Chrome(chrome_options=options)

# 设置超时
browser.set_page_load_timeout(5)
browser.set_script_timeout(10)  # 这两种设置都进行才有效

# 设置窗口大小
browser.set_window_size(1366, 768)

# 访问网站
browser.get("https://www.baidu.com/")

# 截图
browser.save_screenshot("1.png")