'''
@Descripttion: getTargetPicList接口APItest脚本
@Author: Tommy
@Date: 2020-07-17 11:49:37
LastEditors: Tommy
LastEditTime: 2020-08-27 11:07:22
'''
import unittest
import requests
import time
import json
from tool import Tool


class GetTargetPicList(unittest.TestCase):
    '''GetTargetPicList API 测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", "r") as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join(
            [self.__class__.value_dict['url'], 'getTargetPicList_v1'])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getBannerConfig?'
        # pic_list测试数据不能只有一个
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay'],
            "pic_list": "pic_Odsfaw8BI,pic_OIDFUmHt4"
        }

    # def test_getNewsConfig_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getTargetPicList_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, "picName")

    def test_getNewsConfig_success(self):
        '''测试getNewsConfig成功'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertEqual(result['data']['picLength'],
                         len(self.params['pic_list'].split(',')))  # 测试数据不能为一个，否则报错

    def test_getNewsConfig_ios_success(self):
        '''测试IOS getNewsConfig成功'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertEqual(result['data']['picLength'],
                         len(self.params['pic_list'].split(',')))

    def test_getNewsConfig_dateError(self):
        '''测试时间格式错误'''
        self.params['game_date'] = "2020-08-01"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getNewsConfig_ios_dateError(self):
        '''测试IOS 时间格式错误'''
        self.params['game_date'] = "2020-08-01"
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getNewsConfig_requestsError(self):
        '''测试requests错误'''
        del self.params['pic_list']
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: pic_list, error: pic_list is required.")

    def test_getNewsConfig_ios_requestsError(self):
        '''测试IOS requests错误'''
        del self.params['pic_list']
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: pic_list, error: pic_list is required.")

    def test_getNewsConfig_actDayNone(self):
        '''测试参数缺失'''
        self.params['game_actDay'] = ""
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_actDay, error: game_actDay is required.")

    def test_getNewsConfig_ios_actDayNone(self):
        '''测试IOS 参数缺失'''
        self.params['game_actDay'] = ""
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_actDay, error: game_actDay is required.")

    def test_getNewsConfig_type(self):
        '''验证返回值是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getNewsConfig_ios_type(self):
        '''验证IOS 返回值是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getNewsConfig_picList_type(self):
        '''验证图片返回数据格式是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_getNewsConfig_ios_picList_type(self):
        '''验证IOS 图片返回数据格式是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_getNewsConfig_isPicKeyword(self):
        '''验证图片数据关键字是否齐全'''
        keylist = [
            "picName", "picType", "picClass", "picUnlockDate",
            "picVipUnlockDate", "picExpireDate", "picUnlockType",
            "picUnlockNumber", "picJigsawId", "picAssets", "picOrder"
        ]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                             keylist),
                        msg="图片关键字缺失")

    def test_getNewsConfig_ios_isPicKeyword(self):
        '''验证IOS 图片数据关键字是否齐全'''
        keylist = [
            "picName", "picType", "picClass", "picUnlockDate",
            "picVipUnlockDate", "picExpireDate", "picUnlockType",
            "picUnlockNumber", "picJigsawId", "picAssets", "picOrder"
        ]
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                             keylist),
                        msg="图片关键字缺失")

    def test_getNewsConfig_isAssKeyword(self):
        '''验证图片资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword_picAssets(
            result['data']['picList'], keylist),
                        msg="资源关键字缺失")

    def test_getNewsConfig_ios_isAssKeyword(self):
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


if __name__ == '__main__':
    unittest.main()
