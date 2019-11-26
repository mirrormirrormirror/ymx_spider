import requests
import time
username = 'r742953129'
password = 'VNjn5uUJUV'
entry = ('http://customer-%s:%s@tr-pr.oxylabs.io:30001' %
    (username, password))
proxies = { "http": entry[0], "https": entry[0]}
page = requests.get('https://www.amazon.ca/dp/B07FLHJNQ1')
print(page.text)