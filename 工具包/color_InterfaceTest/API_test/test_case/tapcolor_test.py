'''
@Descripttion: getBannerConfig接口APItest脚本
@Author: Tommy
@Date: 2020-06-01 15:47:25
LastEditors: Tommy
LastEditTime: 2020-08-26 16:02:29
'''
import unittest
import requests
import time
import json
from tool import Tool


class GetBannerConfig(unittest.TestCase):
    '''GetBannerconfig API测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join([
            self.__class__.value_dict['new_color_url'],
            'normalApi/v1/getTargetPicList'
        ])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getBannerConfig?'
        self.params = {"pic_list": "pic_EGbUVROpR,pic_pAWnmNx2l"}
        # self.data = dict(pic_list='pic_EGbUVROpR')
        self.url = "https://tapcolor.weplayer.cc/normalApi/v1/getTargetPicList?game_ver=1.3.0&os_type=Android&register_date=20200715&game_date=20200715&game_actDay=1"
        # self.url = "http://httpbin.org/post

    def test_post(self):
        r = requests.post(self.url, data=self.params)
        print(r.text)
        d = Tool.AES_Decrypt("talefuntapcolor!", r.text)
        print(d)


if __name__ == '__main__':
    unittest.main()
