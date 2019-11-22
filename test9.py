import requests
import time
# proxies = { "http": "http://198.50.152.64:23500", "https": "https://198.50.152.64:23500", }
count = 0
countPoint = 0
url = "https://www.google.com/search?sxsrf=ACYBGNQijJp1zP8DrIYLxxx7uIToLlL4mw%3A1574336804346&ei=JHnWXdDgFOPFmAWp9rW4DA&q=python+requests+proxy&oq=python+requests+pro&gs_l=psy-ab.3.0.0j0i203l4j0j0i203j0j0i203j0.699.1661..3205...0.2..0.940.2238.3-1j1j1j1......0....1..gws-wiz.......0i71j35i39j0i67.YEgpl36LGxI"
url1= 'https://www.google.com/search?sxsrf=ACYBGNRsJBKcA526zgF7BB4Ksghf_KC6-g%3A1574394128417&q=inurl%3Awww.amazon.ca%2Fslp+Duplex+Conduit+currently+unavailable'
while True:
    page = requests.get(url1)
    print(page.status_code)
    count = count + 1
    if count - countPoint > 5:
        countPoint = count
        time.sleep(60)
