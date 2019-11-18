import requests

import time

if __name__ == '__main__':
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Referer': "www.google.com"}
    response = session.get('https://www.amazon.ca', headers=headers)
    print(time.time())
    stopCount = 0
    count = 0
    while True:
        page = session.get("https://www.amazon.ca/dp/B07FP5PQYZ/rch")
        print(page.status_code)
        time.sleep(5)
