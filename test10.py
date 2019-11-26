import urllib.request


user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

username = 'r742953129'
password = 'VNjn5uUJUV'
entry = ('http://customer-%s:%s@tr-pr.oxylabs.io:30001' %
    (username, password))

while True:
    query = urllib.request.ProxyHandler({
        'http': entry,
        'https': entry,
    })
    execute = urllib.request.build_opener(query)
    a = execute.open('https://www.amazon.ca/dp/B07FLHJNQ1')
    print(a.status)





# import urllib.request
# import random
# username = 'r742953129'
# password = 'VNjn5uUJUV'
# country = 'DE'
# city = 'munich'
# session = random.random()
# entry = ('http://customer-%s-cc-%s-city-%s:%s@pr.oxylabs.io:7777' %
#     (username, country, city, password))
# query = urllib.request.ProxyHandler({
#     'http': entry,
#     'https': entry,
# })
# execute = urllib.request.build_opener(query)
# print(execute.open('https://www.amazon.ca/dp/B07FLHJNQ1').read())