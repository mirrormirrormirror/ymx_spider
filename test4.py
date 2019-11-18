from Download import Download
from bs4 import BeautifulSoup

if __name__ == '__main__':
    download = Download()
    url = 'https://www.amazon.com/slp/crystal-tree-lighting/rby7do259haa3fm'
    page = download.download(url)
    # print(page.text)
    soup = BeautifulSoup(page.text)
    container = soup.select('.FS-CLP-desktop-page-container')[0]
    linksSoup = container.select('.a-fixed-left-grid-col')
    for linkSoup in linksSoup:
        hrefSoup = linkSoup.select('.a-link-normal')
        if 'a-link-normal' in str(hrefSoup):
            href = hrefSoup[0]['href']
            href = 'https://www.amazon.com' + href
            print(href)


    print(len(linksSoup))



