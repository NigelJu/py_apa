from urllib.request import urlopen 
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import time

class Animal:
    """
        example 共13項
        0: id-'900073000103043',  1: src-'拯救自公立收容所', 
        2: state-'一般', 3: type-'中型', 4: src-'八里保育場試養中',
        5: color'黑', 6: race'犬類', 7: feature'虎斑腳', 
        8: name'貝爾', 9: view'短毛', 10: gender'母', 
        11: personality'乖巧溫馴', 12: birth'2017年', 
        13: comment'']
    """
    def __init__(self,chip_id = "", keeps = [], details = []):
        self.chip_id = chip_id
        self.keeps = keeps
        self.details = details

    def images(self, *imgs):
        return self.images

APA_URL = "http://www.apatw.org/"
ALL_ANIMALS_URL = APA_URL + "All_animal.asp"
FIND_PAGE_URL = "http://www.apatw.org/All_animal.asp?an_chipcode=&an_color=&an_name=&an_zone=&user_name=&GetPass=-1&intCurPage="

def get_bsObj(url):
    try:
        html = urlopen(url, timeout=10)
        bsObj =  BeautifulSoup(html.read())
        return bsObj
    except HTTPError as e:
        return None
    except socket.timeout as e: # <-------- this block here
        print("Time Out")
        return None

# 取得特定網址的動物資料
def animals_per_page(url):
    bs_obj = get_bsObj(url)
    # 取得可飼養狗的表格
    dog_table = bs_obj.findAll("table", {"width": "180", "cellpadding": "0"})

    dog_chip_code_regex = "(Show_Animal)"
    animals = []

    for dog_detail in dog_table:
        # 取得所有狗的詳細網址
        dog_a = dog_detail.find("a", {"href": re.compile(dog_chip_code_regex)})
        dog_chip_id = ""

        # 沒ID就繼續找
        if dog_a is None:
            continue

        # 取得飼養人名稱
        keepers = dog_detail.findAll("font", {"color": "#009900"})
        dog_keepers = []
        for keep in keepers:
            dog_keepers.append(keep.get_text(strip = True))

        # 取得詳細資料
        dog_chip_id = dog_a["href"]
        animal = fetch_detail_animal(dog_chip_id, dog_keepers)
        animals.append(animal)

    return(animals)

# 取得動物資料的最後一頁的頁碼
def get_last_page(url):
    page_regex = "(an_chipcode=&an_color=&an_name=&an_zone=&user_name=&GetPass=-1&intCurPage)"
    bsObj = get_bsObj(url)
    href = bsObj.find("a", {"href": re.compile(page_regex)})
    td = href.parent.get_text(strip = True)
    # 會拿到文字, 想直接濾出數字來
    numbers = [int(s) for s in td.split() if s.isdigit()]
    # 會取得最後一頁的頁碼以及總資料筆數
    return numbers[0]

def fetch_detail_animal(url, keepers):
    url = APA_URL + url
    bsObj = get_bsObj(url)

    # 找到狗的相關資訊
    dog_infos_html = bsObj.find_all("td", {"class": "browntxt2", "scope": "col"})
    dog_infos = []
    for dog_info_html in dog_infos_html:
        dog_infos.append(dog_info_html.get_text(strip = True))

    animal = Animal(str(dog_infos[0]), keepers, dog_infos)

    # 找到狗的圖片網址
    dog_imgs_regex = "(/UploadFile)"
    dog_images = bsObj.findAll("img", {"src": re.compile(dog_imgs_regex)})
    dog_imgs_url = []
    for image in dog_images:
        img_url = APA_URL + image["src"]
        dog_imgs_url.append(img_url)

    animal.images = dog_imgs_url

    return animal


def fetch_animals():
    # range範圍為 start <= index < end, 所以要+1, 不然會少最後一頁
    last_page = get_last_page(ALL_ANIMALS_URL) + 1
    animals = []
   
    """
    range記得改
    """
    for website_index in range(1,last_page):
        if website_index % 3 == 0:
            time.sleep(15)
            print(website_index)
        print(website_index)
        new_website = FIND_PAGE_URL + str(website_index)
        animals.extend(animals_per_page(new_website))
    return animals




# fetch_animals()