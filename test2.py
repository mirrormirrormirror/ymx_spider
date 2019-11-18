#coding=utf-8
import requests

#请求地址
targetUrl = "https://www.amazon.com/Wireless-Headphones-Bluetooth-Earphones-Microphone/dp/B076TZ8HD3"

#代理服务器
proxyHost = "61.145.48.141"
proxyPort = "9999"

header = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'referer': 'http://www.google.com',
            'Cookie': 'session-id=142-1856658-2896406; session-id-time=2082787201l; ubid-main=131-8710692-7468333; skin=noskin; a-ogbcbff=1; session-token="ZTEg96lAjUpWE7IzwG1kee3ZHDmqsmGWky2Jm+4/dAh53BOlCTBL5obuams3t2bKB9+kmlMwZ96uuhqm3jbfC2MfnUcRKmf5nd/65ZsN4ftjItNMZDbsS1MP82bQ0gWBArC/QHD97quwx8JJcu4W/Vnol96Di+GUh8LWBmSl+9yMQzhV34OfRydooxkt2fAt+qgvfg9glmb1QbZlz6fb5k1RkXlK2V32rohhJv9pxbQ="; x-main="f7xSJd64ckBI?bH2FbDfcPija9NyYM1YNJWoxgdopH0tM6wiEUGG0@03LcEjB9gD"; at-main=Atza|IwEBIOhxw4oqwhGjgatHVAK5Qzcg6AAsVjAbNc7leaF2Hkn2MrhCLdaRlPrxMG2KwcQMxYK7O2q75bEGLV1uboy2P3TT2qFo8ATytA_9YTbvPVtFrqTG4AWORKzI-B_u8oB0GxsHTz6QK3K-JWJsoRke77S_0kTnatVjhfBYA4qABAa7LyNQkOMPiWc7zFH5IooDijPQ7Qh8-G-Dya0-KzMDWNeliiJyUr497ZXAItpV-jXFCsHeHNAL_JNiKd5ZpWDrfllLE5LFATEg7QmNG8vgG56APTC9Ytiqyv6Uo6urLCd5P-RVn743B7vEaWDhI8FEG0C9lwcr2DHGSNigojjpMMbb_gTCTosW2cSD_3LKV4k7HWLcwNjJGB6mhXVX-n2Pw_e1XjYSxG3h3Krd1QVRmZi7chs7ozEO9cZ5LLjmyKlm79g6XerLA_9zuNUQ2OD5cTw; sess-at-main="XWfprTCn/L93F7JPFzWV96NdA8S7r8echY0gsZgGowo="; sst-main=Sst1|PQFUR675t7_XpG1dMhfu5puGC0rsvJq1oyeS9hJJrJv4_ouPUEjhZx32JUMFEZzm1EFczmYEMBrwXguP9-4Zj-hMa_3iIFRbAB58wNeLCZAv9qWvfYyokDqQB5YnO8PhqoTINhpZ_NAzDps9Wj7Ct3BzAbj6LtfNUnVLxXGC-axiElOQgYIJAwJ5Yc4R2tdRqmHQfy4Ax7H4VIT6l2wzJONSokZueOLUFIVkRWueErL3VJD7a5ZnUx0c9Pu2I2Ze_hnvgI7vPaAppQ0yOBgmt0LHb5lOLDPVPsZlfOeGZarNqiWW4u1AP2jEG5tuG74SLp923cDiXSnns2Tn5f7ZDNkl8Q; lc-main=en_US; i18n-prefs=USD; x-wl-uid=1OPCDRe/Atic1M8g5ilOnFflNGEIbBSQMPbCxrLpbZ7PDoEFJPeqF2j2sihyJ0T2SxzRod3bwHCCsayHMhXhtj5y5rHZQODfQNUlfeEE4U2GB0Pavdj3m4GGYSXqiolf36MpaD2nNYQg=; sp-cdn="L5Z9:CN"; csm-hit=tb:s-BGC8MB9EX91NM79NEPJK|1573826969786&t:1573826971616&adb:adblk_no'
        }


proxyMeta = "http://%(host)s:%(port)s" % {

    "host" : proxyHost,
    "port" : proxyPort,
}



#pip install -U requests[socks]  socks5代理
# proxyMeta = "socks5://%(host)s:%(port)s" % {

#     "host" : proxyHost,

#     "port" : proxyPort,

# }

proxies = {
    "http"  : proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies,headers=header)
print (resp.status_code)
print (resp.text)