import requests

# 要访问的目标页面
targetUrl = "https://www.amazon.com/Wireless-Headphones-Bluetooth-Earphones-Microphone/dp/B076TZ8HD3"
# targetUrl = "http://proxy.abuyun.com/switch-ip"
# targetUrl = "http://proxy.abuyun.com/current-ip"

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H29T984763248B9D"
proxyPass = "F323325CFBD63556"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'referer': 'https://www.amazon.com',
            'Cookie': 'session-id-time=2082787201l; path=/; domain=.amazon.com; expires=Tue, 01-Jan-2036 08:00:01 GMT'
        }

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies,headers=header)

print(resp.status_code)
print(resp.text)
