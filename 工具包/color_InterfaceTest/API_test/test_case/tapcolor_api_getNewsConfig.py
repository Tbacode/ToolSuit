'''
@Descripttion: getNewsConfig接口APItest脚本
@Author: Tommy
@Date: 2020-07-16 16:46:09
@LastEditors: Tommy
@LastEditTime: 2020-07-31 17:09:51
'''
import unittest
import requests
import time
import json
from tool import Tool


class GetNewsConfig(unittest.TestCase):
    '''GetNewsConfig API测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join(
            [self.__class__.value_dict['url'], 'getNewsConfig_v1'])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getBannerConfig?'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay']
        }

    # def test_getNewsConfig_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getNewsConfig_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, "picId")

    def test_getNewsConfig_success(self):
        '''测试getNewsConfig成功'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['newsList']), 0)

    def test_getNewsConfig_ios_success(self):
        '''测试IOS getNewsConfig成功'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['newsList']), 0)

    def test_getNewsConfig_requestsError(self):
        '''测试requests错误'''
        del self.params['game_ver']
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_ver, error: game_ver is required.")

    def test_getNewsConfig_ios_requestsError(self):
        '''测试IOS requests错误'''
        del self.params['game_ver']
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_ver, error: game_ver is required.")

    def test_getNewsConfig_dateError(self):
        '''测试日期格式错误'''
        self.params['game_date'] = "2020-06-06"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getNewsConfig_ios_dateError(self):
        '''测试IOS 日期格式错误'''
        self.params['game_date'] = "2020-06-06"
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

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

    def test_getNewsConfig_newsListType(self):
        '''验证event数据是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['newsList'], dict))

    def test_getNewsConfig_ios_newsListType(self):
        '''验证IOS event数据是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['newsList'], dict))


if __name__ == '__main__':
    unittest.main()
