'''
@Descripttion: getBannerConfig接口APItest脚本
@Author: Tommy
@Date: 2020-06-01 15:47:25
@LastEditors: Tommy
@LastEditTime: 2020-07-31 18:06:48
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
        self.url = ''.join(
            [self.__class__.value_dict['url'], 'getBannerConfig_v1'])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getBannerConfig?'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay']
        }

    def test_getBannerConfig_success(self):
        '''测试getBannerConfig接口成功'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['bannerList']), 0)

    def test_getBannerConfig_ios_success(self):
        '''测试IOS getBannerConfig接口成功'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['bannerList']), 0)

    def test_getBannerConfig_requestsError(self):
        '''测试requests错误'''
        del self.params['game_date']
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_date, error: game_date is required.")

    def test_getBannerConfig_ios_requestsError(self):
        '''测试IOS requests错误'''
        del self.params['game_date']
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_date, error: game_date is required.")

    # def test_bannerconfig_new_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getBannerConfig_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, "action")

    def test_getBannerConfig_dateError(self):
        '''测试日期格式错误'''
        self.params['game_date'] = "0"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getBannerConfig_ios_dateError(self):
        '''测试IOS 日期格式错误'''
        self.params['game_date'] = "0"
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getBannerConfig_type(self):
        '''验证返回值格式是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getBannerConfig_ios_type(self):
        '''验证IOS 返回值格式是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getBannerConfig_listType(self):
        '''验证bannerList下是否格式正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['bannerList'], dict),
                        msg='子项格式错误')

    def test_getBannerConfig_ios_listType(self):
        '''验证IOS bannerList下是否格式正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['bannerList'], dict),
                        msg='子项格式错误')


if __name__ == '__main__':
    unittest.main()
