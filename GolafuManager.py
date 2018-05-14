from urllib.request import urlopen 
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver

GOLAFU_URL = "http://golafu.apatw.org/longstay"

class Golafu:
    def __init__(self, title = "", album_url = [], visits_url = [], visitors = []):
        self.title = title
        self.album_url = album_url
        self.visits_url = visits_url
        self.visitors = visitors

def get_bsObj(url):
    try:
        html = urlopen(url, timeout=10)
        bsObj =  BeautifulSoup(html.read())
        return bsObj
    except HTTPError as e:
        return None
    except socket.timeout as e:
        print("Time Out")
        return None

def get_areas():
    golafu_longstay = get_bsObj(GOLAFU_URL)
    areas = golafu_longstay.findAll("area")
    areas_url = []
    for area in areas:
        areas_url.append(area["href"])
    return areas_url

def get_golafus():
    areas = get_areas()
    driver = webdriver.Safari()
    golafus = []
    for index, area in enumerate(areas):
        # if index > 3:
        #     break
        detail = get_bsObj(area)
        title = detail.find("span", {"id": "sites-page-title"}).get_text()
        print(title)
        visit_records = detail.find_all("li", {"style": "list-style-position:outside;list-style-type:circle"})
        urls = []
        visitors = []
        for visit_record in visit_records:
            url = visit_record.find("a")["href"]
            visitor = visit_record.get_text()
            urls.append(url)
            visitors.append(visitor)

        #使用selenium點選iframe, 並取得新分頁網址#
        driver.get(area)
        iframe = driver.find_element_by_tag_name("iframe")
        driver.switch_to_frame(iframe)
        urls_in_iframe = driver.find_elements_by_xpath("//@href")
        album_url = ""
        if len(urls_in_iframe) > 0:
            album_url = urls_in_iframe[0].text
        print(album_url)
       
        golafu = Golafu(title=title, album_url=album_url, visits_url=urls, visitors=visitors)
        golafus.append(golafu)

    driver.close()
    return golafus
    

# get_golafus()