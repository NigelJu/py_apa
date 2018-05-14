import ApaManager as apa_manager
import GolafuManager as golafu_manager
import GoogleSheetManager as google_sheet_manager
import time

def get_str_by_list(ori_list):
    return ','.join(str(e) for e in ori_list)


def update_GOLAFU():
    golafus = golafu_manager.get_golafus()
    for (index, golafu) in enumerate(golafus):
        if index % 5 == 0:
            time.sleep(5)
        print(golafu.title)
        print(golafu.album_url)
        print("==")
        range_name = "A"+str(index+2)
        visitor_url_list = get_str_by_list(golafu.visits_url)
        vistor_list = get_str_by_list(golafu.visitors)
        data = [golafu.title, golafu.album_url, visitor_url_list, vistor_list]
        google_sheet_manager.write_GOLAFU_with_range(data, range_name)

def update_APA():
    animals = apa_manager.fetch_animals()
    for (index, animal) in enumerate(animals):
        if index % 5 == 0:
            time.sleep(5)
        print(animal.chip_id)
        print(animal.keeps)
        print("==")
        range_name = "A"+str(index+2)
        # 直接把所有資料縮成一條List, 交由別人去做寫入的動作
        # keepers, images要拉出變一條字串
        images = get_str_by_list(animal.images)
        keepers = get_str_by_list(animal.keeps)
        # datas = [animal.chip_id, keepers, images]
        datas = [keepers, images]
        datas.extend(animal.details)
        google_sheet_manager.write_APA_with_range(datas, range_name = range_name)



# update_APA()
update_GOLAFU()
