'''
@Descripttion: getGallery接口APItest脚本
@Author: Tommy
@Date: 2020-05-27 16:38:30
@LastEditors: Tommy
@LastEditTime: 2020-07-31 18:14:29
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
        self.url = ''.join(
            [self.__class__.value_dict['url'], 'getGalleryList_v1'])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getGalleryList'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay'],
            "pic_type": "All",
            "start_date": self.start_date
        }
        # 代理设置，避免ip被封
        # self.proxies={'http':'http://125.118.146.222:6666'}

    def test_gallery_success(self):
        '''测试gallery成功'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(result['data']['picLength'], 0)

    def test_gallery_ios_success(self):
        '''测试IOS gallery成功'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(result['data']['picLength'], 0)

    def test_gallery_requestError(self):
        '''测试request参数异常'''
        del self.params['game_date']
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_date, error: game_date is required.")

    def test_gallery_ios_requestError(self):
        '''测试IOS request参数异常'''
        del self.params['game_date']
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_date, error: game_date is required.")

    def test_gallery_dateError(self):
        '''测试日期数据错误'''
        self.params['start_date'] = "2020-05-08"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: start_date, error: start_date must have a length between 8 and 8."
        )

    def test_gallery_ios_dateError(self):
        '''测试IOS 日期数据错误'''
        self.params['start_date'] = "2020-05-08"
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: start_date, error: start_date must have a length between 8 and 8."
        )

    def test_gallery_pictypeError(self):
        '''测试图片分类为空'''
        self.params['pic_type'] = ""
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: pic_type, error: pic_type is required.")

    def test_gallery_ios_pictypeError(self):
        '''测试IOS 图片分类为空'''
        self.params['pic_type'] = ""
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: pic_type, error: pic_type is required.")

    # def test_gallery_new_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     # self.params['start_date'] = "20200718"
    #     self.params['pic_type'] = "Jigsaw"
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getGalleryList_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, "picName")

    def test_gallery_type(self):
        '''验证返回值是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_gallery_ios_type(self):
        '''验证IOS 返回值是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_gallery_picList_type(self):
        '''验证图片返回数据格式是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_gallery_ios_picList_type(self):
        '''验证IOS 图片返回数据格式是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_gallery_isPicKeyword(self):
        '''验证图片数据关键字是否齐全'''
        keylist = [
            "picName", "picType", "picClass", "picUnlockDate",
            "picVipUnlockDate", "picExpireDate", "picUnlockType",
            "picUnlockNumber", "picJigsawId", "picAssets"
        ]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                             keylist),
                        msg="图片关键字缺失")

    def test_gallery_ios_isPicKeyword(self):
        '''验证IOS 图片数据关键字是否齐全'''
        keylist = [
            "picName", "picType", "picClass", "picUnlockDate",
            "picVipUnlockDate", "picExpireDate", "picUnlockType",
            "picUnlockNumber", "picJigsawId", "picAssets"
        ]
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                             keylist),
                        msg="图片关键字缺失")

    def test_gallery_isAssKeyword(self):
        '''验证图片资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword_picAssets(
            result['data']['picList'], keylist),
                        msg="资源关键字缺失")

    def test_gallery_ios_isAssKeyword(self):
        '''验证IOS 图片资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword_picAssets(
            result['data']['picList'], keylist),
                        msg="资源关键字缺失")

    def test_gallery_pictype_check(self):
        '''验证图片类型是否符合请求'''
        pictype_list = [
            "Jigsaw", "Animated", "Special", "Character", "Animal", "Flower",
            "Places", "Nature", "Message", "Mosaic", "Mandala", "Other"
        ]
        self.params['pic_type'] = pictype_list[random.randint(
            0, len(pictype_list))]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_pic_type(result['data']['picList'],
                                            self.params['pic_type']),
                        msg="{}类型存在异常".format(self.params['pic_type']))

    def test_gallery_ios_pictype_check(self):
        '''验证IOS 图片类型是否符合请求'''
        pictype_list = [
            "Jigsaw", "Animated", "Special", "Character", "Animal", "Flower",
            "Places", "Nature", "Message", "Mosaic", "Mandala", "Other"
        ]
        self.params['pic_type'] = pictype_list[random.randint(
            0, len(pictype_list))]
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_pic_type(result['data']['picList'],
                                            self.params['pic_type']),
                        msg="{}类型存在异常".format(self.params['pic_type']))


if __name__ == '__main__':
    unittest.main()
    # suite = TestSuite()
    # suite.addTest(GetGalleryList('test_gallery_pictype_check'))
    # unittest.TextTestRunner().run(suite)
