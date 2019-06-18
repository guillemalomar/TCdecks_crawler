from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
from urllib import request


def obtain_page(url):
    cj = CookieJar()
    cp = request.HTTPCookieProcessor(cj)
    try:
        opener = request.build_opener(cp)
        with opener.open(url, timeout=1000) as response:
            soup = BeautifulSoup(response.read())
    except:
        soup = None
    return soup
