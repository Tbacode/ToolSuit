'''
@Descripttion: 新color getLanguage接口APItest脚本
@Author: Tommy
@Date: 2020-06-02 16:01:55
LastEditors: Tommy
LastEditTime: 2020-08-24 17:42:28
'''
import unittest
import time
import json
from tool import Tool


class GetLanguage_new(unittest.TestCase):
    """Language API测试"""
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join([
            self.__class__.value_dict['new_color_url'],
            'normalApi/v1/getLanguage'
        ])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getLanguage?'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay'],
            "language_key": "ChineseSimplified",
            "language_version": "-1",
            "forece_get": "1"
        }

    # def test_getLanguage_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getLanguage_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, "language")

    def test_new_getLanguage_success(self):
        '''测试新color Language成功'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['language']),
                            0,
                            msg="language数据为空")

    def test_new_getLanguage_ios_success(self):
        '''测试新color IOS Language成功'''
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['language']),
                            0,
                            msg="language数据为空")

    def test_new_getLanguage_languageNone(self):
        '''测试新color 参数缺失'''
        self.params['language_key'] = ""
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: language_key, error: language_key is required.")

    def test_new_getLanguage_ios_languageNone(self):
        '''测试新color IOS 参数缺失'''
        self.params['language_key'] = ""
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: language_key, error: language_key is required.")

    def test_new_getLanguage_dateError(self):
        '''测试新color 日期格式错误'''
        self.params['game_date'] = "2020-05-29"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_new_getLanguage_ios_dateError(self):
        '''测试新color IOS 日期格式错误'''
        self.params['game_date'] = "2020-05-29"
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_new_getLanguage_requestsError(self):
        '''测试新color requests错误'''
        del self.params['game_ver']
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_ver, error: game_ver is required.")

    def test_new_getLanguage_ios_requestsError(self):
        '''测试新color IOS requests错误'''
        del self.params['game_ver']
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_ver, error: game_ver is required.")

    def test_new_getLanguage_type(self):
        '''验证新color 返回值是否正确'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['language']),
                            0,
                            msg="language数据为空")
        self.assertIsInstance(result['data']['language'], dict)

    def test_new_getLanguage_ios_type(self):
        '''验证新color IOS 返回值是否正确'''
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['language']),
                            0,
                            msg="language数据为空")
        self.assertIsInstance(result['data']['language'], dict)


if __name__ == '__main__':
    unittest.main()
