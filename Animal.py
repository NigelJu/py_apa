from urllib.request import urlopen 
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv
import re

class Animal:
    def __init__(self,chip_id = "", keeps = []):
        self.chip_id = chip_id
        self.keeps = keeps


def get_bsObj(url):
    try:
        html = urlopen(url)
        bsObj =  BeautifulSoup(html.read())
        return bsObj
    except HTTPError as e:
        return None

website = "http://www.apatw.org/All_animal.asp"
# website = "http://www.apatw.org/All_animal.asp?an_chipcode=&an_color=&an_name=&an_zone=&user_name=&GetPass=-1&intCurPage=40"

bs_obj = get_bsObj(website)
# 取得可飼養狗的表格
dog_table = bs_obj.findAll("table", {"width": "180", "cellpadding": "0"})

dog_chip_code_regex = "(Show_Animal)"

animals = []

dog_count = 0
for dog_detail in dog_table:
    # 取得所有狗的詳細網址
    dog_a = dog_detail.find("a", {"href": re.compile(dog_chip_code_regex)})
    dog_chip_id = ""

    # 沒ID就繼續找
    if dog_a is None:
        continue

    dog_chip_id = dog_a["href"]
    print("==============")

    # 取得飼養人名稱
    keeper_regex = "images/logo_heart_26.gif"
    keepers = dog_detail.findAll("font", {"color": "#009900"})
    dog_keepers = []
    for keep in keepers:
        dog_keepers.append(keep.get_text(strip = True))

    animal = Animal(dog_chip_id, dog_keepers)
    animals.append(animal)


print(len(animals))
for animal in animals:
    print(animal.keeps)
    print(animal.chip_id)

# print(dog_count)
# """



# 取得狗的飼養人
# for dog_detail in dog_table:
#     print(dog_detail)

"""
sum = 0
for dog_detail in dog_table:
    
    # 取得晶片號碼及飼養人
    # 資料格式為
    # [0] 晶片號碼
    # [1] dog_info
    # [2..] 飼養人

    dog_all_tr = dog_detail.findAll("td", {"height": "24"})
    for index, dog_tr in enumerate(dog_all_tr):
        print("========= " + str(index) + " ============")
        print(dog_tr.get_text())
        sum += 1
        print(dog_tr)
        if dog_tr.has_attr("href"):
            print("yes")
       
        # 取得狗的詳細資料(進入detail頁面)

"""
    

# detail網址 = website + an_chipcode=晶片號碼

print(sum)
# print(dog_infos.get_text())



# for index, dog_info in enumerate(dog_infos):
#     sum += 1
#     print(index)
#     print(dog_info.get_text())

# print(sum)
# print(dog_table)