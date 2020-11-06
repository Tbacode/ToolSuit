'''
Descripttion: 验证正式上线前，pic数据得一致性
Author: Tommy
Date: 2020-11-05 15:24:58
LastEditors: Tommy
LastEditTime: 2020-11-06 15:36:54
'''

# TODO: 引包
import requests
import time
import datetime
import random
import json


class PicCheck():
    def __init__(self, url: str, game_ver: str, os_type: str):
        self.pic_list_item = []
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.start_date = time.strftime("%Y%m%d", time.localtime())
        self.url = url
        self.params = {
            "game_ver": game_ver,
            "os_type": os_type,
            "register_date": self.start_date,
            "game_date": self.game_date,
            "game_actDay": 1,
            "pic_type": "All",
            "start_date": self.start_date,
            "group_id": random.randint(0, 99)
        }

    # TODO: 请求数据返回数据
    def request_pic_list_item(self) -> dict:
        print("开始请求数据")
        pic_item = requests.get(self.url, params=self.params)
        # pic_item = json.dumps(pic_item.json(),
        #                       indent=2,
        #                       sort_keys=False,
        #                       ensure_ascii=False)
        pic_item = pic_item.json()
        return pic_item

    # TODO: 判断是否isEnd
    def isEnd_check(self):
        print("开始判断是否结束")
        result = self.request_pic_list_item()
        if bool(result['data']['isEnd']):
            return True
        else:
            dict_item = self.get_keyword_json(result['data']['picList'])
            self.add_pic_list(dict_item)
            return False

    # TODO: 构造关键字提取数据
    def get_keyword_json(self, list_item: list) -> dict:
        print("开始构造数据")
        dict_item_list = []
        for pic_item in list_item:
            dict_item = {}
            dict_item['picName'] = pic_item['picName']
            dict_item['picType'] = pic_item['picType']
            dict_item['picClass'] = pic_item['picClass']
            dict_item['picUnlockDate'] = pic_item['picUnlockDate']
            dict_item['picVipUnlockDate'] = pic_item['picVipUnlockDate']
            dict_item['picExpireDate'] = pic_item['picExpireDate']
            dict_item['picUnlockType'] = pic_item['picUnlockType']
            dict_item['picUnlockNumber'] = pic_item['picUnlockNumber']
            dict_item['picJigsawId'] = pic_item['picJigsawId']
            dict_item['picOrder'] = pic_item['picOrder']
            dict_item['picComicId'] = pic_item['picComicId']
            dict_item['picComicKey'] = pic_item['picComicKey']
            dict_item = json.dumps(dict_item,
                                   sort_keys=False,
                                   indent=2,
                                   ensure_ascii=False)
            dict_item_list.append(dict_item)
        return dict_item_list

    # TODO: 数据追加
    def add_pic_list(self, pic_list: list) -> list:
        '''
        @name: add_pic_list
        @msg: 只是追加数据
        @param {*}
        @return {*}
        '''
        print("数据追加")
        return self.pic_list_item.append(pic_list)

    # TODO: 主循环
    def main_function(self):
        if self.isEnd_check():
            return
        else:
            # 日期减一天
            print("日期减一")
            # TODO: 日期格式调整，使请求日期格式正确，功能正常
            now = self.params['start_date']
            delta = datetime.timedelta(days=1)
            n_days = now - delta
            self.params['start_date'] = n_days.strftime('%Y%m%d')
            print("请求日期：" + self.params['start_date'])
            print("递归")
            self.main_function()


# TODO: main function
if __name__ == "__main__":
    url = "https://us-central1-tapcolor-new-debug.cloudfunctions.net/normalApi/"
    url = ''.join([url, 'normalApi/v1/getGalleryList'])
    game_ver = "4.7.0"
    os_type = "Android"
    pic_check = PicCheck(url, game_ver, os_type)
    # pic_check.isEnd_check()
    # print(pic_check.pic_list_item)
    # print(pic_check.start_date)
    pic_check.main_function()
    print(pic_check.pic_list_item)
