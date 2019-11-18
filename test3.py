import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import re
import time
import sys


def recognize_code_image(image_file='image\\captcha_code_01.png'):
    """
    识别图片上的验证码,这个步骤真是蛋疼死人了，现在一定要折腾到底
    1. 早先不知道pytesseract这个库还需要一个pytesser，所以运行image_to_string总是出错，根本就得不到验证码，哪怕是错的验证码
    2. 后来知道了这个pytesser，但却不知道怎么用，一度忽略了它，以为是其他地方出问题了
    3. 终于，我知道了，这个pytesser就像是driver的驱动器一样，需要让pytesseract识别，只是，大家没拿到明面上说，代码里面也没有明确的体现
    4.
    """
    # 打开图片
    image = Image.open(image_file)
    # image.show()
    # 转为灰度图片
    image_grey = image.convert('L')
    # image_grey.show()
    # 二值化
    table = []
    for i in range(256):
        if i < 140:
            table.append(0)
        else:
            table.append(1)
    image_bi = image_grey.point(table, '1')
    # 识别验证码
    verify_code = pytesseract.image_to_string(image_bi)
    print(verify_code)
    return verify_code


def parseMeta(text):
    soup = BeautifulSoup(text)
    src = soup.select('div.a-row.a-text-center > img')[0]['src']
    print(src)
    # page = requests.get(src)
    # img = page.content
    # timestape = time.time()
    # imageDir = 'image/' + str(timestape) + '.jpg'
    # with open(imageDir, 'wb') as f:
    #     f.write(img)
    # f.close()
    # print('finish')

    keyword = inputKeywordFile()
    amznPattern = 'amzn" value="(.*?)"'
    amznGroup = re.search(amznPattern, text)
    amznStr = amznGroup.group()
    amznStr = amznStr.replace('amzn" value="', '')
    amznStr = amznStr.replace('"', '')
    amznR = '/dp/B07FSQPT54'
    meta = {'amzn': amznStr, 'amznR': amznR, 'field-keywords': keyword}
    return meta


def inputKeywordFile():
    keywordFile = input("input keywordFile: ")
    return keywordFile


if __name__ == '__main__':

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.44.77 Safari/537.36',
        'Referer': "https://www.amazon.com/slp/crystal-tree-lighting/rby7do259haa3fm"
    }

    proxyHost = "117.30.112.152"
    proxyPort = "9999"

    proxyMeta = "http://%(host)s:%(port)s" % {

        "host": proxyHost,
        "port": proxyPort,
    }
    proxies = {
        "http": proxyMeta,
    }

    session = requests.session()

    page = session.get(
        'https://www.amazon.com/Cherry-Blossom-Decals-Nursery-Flower/dp/B00KAXI67Q?ref_=fsclp_pl_dp_6',
        headers={},cookies={})

    count = 0
    print(page.text)

    if 'nter the characters you see below' in page.text:
        print(page.text)
        meta = parseMeta(page.text)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.44.77 Safari/537.36',

        }
        a = requests.get(url='https://www.amazon.com/errors/validateCaptcha', data=meta)
        print(a.status_code)
        page = requests.get('https://www.amazon.com/dp/B07FSQPT54')
        print(page.text)
