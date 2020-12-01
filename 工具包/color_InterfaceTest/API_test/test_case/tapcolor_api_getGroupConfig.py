'''
@Descripttion: getGroupConfig接口APItest脚本
@Author: Tommy
@Date: 2020-06-12 15:52:55
LastEditors: Tommy
LastEditTime: 2020-10-20 18:07:31
'''
import unittest
import requests
import time
import random
import json
# from tool import Tool


class GetGroupConfig(unittest.TestCase):
    '''GroupConfig API测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join(
            [self.__class__.value_dict['url'], 'normalApi/v1/getGroupConfig'])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getGroupConfig'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay'],
            "group_id": random.randint(0, 99)
        }

    def test_Group_success(self):
        '''测试Group成功'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']), 0, msg="GourpID = {}".format(self.params['group_id']))
        self.assertEqual(len(result['errorMsg']), 0)

    def test_Group_ios_success(self):
        '''测试IOS Group成功'''
        r = requests.get(self.url, params=self.params)
        self.params['os_type'] = "Ios"
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']), 0, msg="GourpID = {}".format(self.params['group_id']))
        self.assertEqual(len(result['errorMsg']), 0)

    def test_Group_IdError(self):
        '''测试ID错误'''
        self.params['group_id'] = 1000
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: group_id, error: group_id must have a length between 1 and 3."
        )

    def test_Group_ios_IdError(self):
        '''测试IOS ID错误'''
        self.params['group_id'] = 1000
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: group_id, error: group_id must have a length between 1 and 3."
        )

    def test_Group_OsTypeError(self):
        '''测试os_type错误'''
        self.params['os_type'] = -1
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: os_type, error: os_type must be either Android, Ios, Mac or Windows."
        )

    def test_Group_dateError(self):
        '''测试时间格式错误'''
        self.params['game_date'] = "2020-06-07"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_Group_ios_dateError(self):
        '''测试IOS 时间格式错误'''
        self.params['game_date'] = "2020-06-07"
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    # def test_getGroupConfig_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getGroupConfig_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, None)

    def test_getGroupConfig_type(self):
        '''验证返回值是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getGroupConfig_ios_type(self):
        '''验证IOS 返回值是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
