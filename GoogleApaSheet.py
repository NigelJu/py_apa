import ApaManager as apa_manager
import GoogleSheetManager as google_sheet_manager
import time

def get_str_by_list(ori_list):
    return ','.join(str(e) for e in ori_list)



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
    datas = [animal.chip_id, keepers, images]
    datas.extend(animal.details)
    google_sheet_manager.write_data_with_range(datas, range_name = range_name)



