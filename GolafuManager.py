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


#####

areas = get_areas()

driver = webdriver.Safari()
golafus = []
for index, area in enumerate(areas):
    print("第" + str(index) + "筆")
    print("網址是" + area)

    detail = get_bsObj(area)
    title = detail.find("span", {"id": "sites-page-title"}).get_text()
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
    time.sleep(5)
    iframe.click()
    time.sleep(5)
    handles = driver.window_handles

    if len(handles) == 1:
        print("現在處理的分頁")
        print(driver.title)
        print(handles)
        print("無法取得網址")
        continue

    driver.switch_to.window(handles[1])
    time.sleep(5)
    album_url = driver.current_url

    driver.close()

    golafu = Golafu(title=title, album_url=album_url, visits_url=urls, visitors=visitors)
    golafus.append(golafu)

print("結束了")
    
for golafu in golafus:
    print(golafu.album_url)