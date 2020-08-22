'''
Description: new color GetGalleryAPI测试
Autor: Tommy
Date: 2020-08-23 01:24:37
LastEditors: Tommy
LastEditTime: 2020-08-23 01:55:04
'''
import unittest
import requests
import time
import json
from tool import Tool
import random
# from unittest import TestSuite
# from urllib import parse


class GetGalleryList(unittest.TestCase):
    '''GalleryList API测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.start_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join([
            self.__class__.value_dict['new_color_url'],
            'normalApi/v1/getGalleryList'
        ])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getGalleryList'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay'],
            "pic_type": "All",
            "start_date": self.start_date,
            "group_id": random.randint(0, 99)
        }
        # 代理设置，避免ip被封
        # self.proxies={'http':'http://125.118.146.222:6666'}

    def request_get_result(self, url, parm):
        r = requests.get(url, params=parm)
        aes_result = Tool.AES_Decrypt("talefuntapcolor!", r.text)
        result = json.loads(aes_result)
        return result

    def test_one(self):
        result = self.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)


if __name__ == '__main__':
    unittest.main()
