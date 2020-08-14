'''
@Descripttion: getDeeplinkPicConfig接口APItest脚本
@Author: Tommy
@Date: 2020-07-17 11:35:59
@LastEditors: Tommy
@LastEditTime: 2020-07-31 18:06:06
'''
import unittest
import requests
import time
import json
from tool import Tool


class GetDeeplinkPicConfig(unittest.TestCase):
    '''GetDeeplinkPicConfig API 测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join(
            [self.__class__.value_dict['url'], 'getDeeplinkPicConfig_v1'])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getBannerConfig?'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay'],
            "event_id": "CLGPUWSbDD"
        }

    # def test_getDeeplinkPicConfig_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getDeeplinkPicConfig_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, "picId")
    #     print(result2)

    def test_getDeeplinkPicConfig_dateError(self):
        '''测试日期格式错误'''
        self.params['game_date'] = "2020-05-29"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getDeeplinkPicConfig_ios_dateError(self):
        '''测试IOS 日期格式错误'''
        self.params['game_date'] = "2020-05-29"
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getDeeplinkPicConfig_requestsError(self):
        '''测试requests错误'''
        del self.params['event_id']
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: event_id, error: event_id is required.")

    def test_getDeeplinkPicConfig_ios_requestsError(self):
        '''测试IOS requests错误'''
        del self.params['event_id']
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: event_id, error: event_id is required.")

    def test_getDeeplinkPicConfig_eventNone(self):
        '''测试参数缺失'''
        self.params['event_id'] = ""
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: event_id, error: event_id is required.")

    def test_getDeeplinkPicConfig_ios_eventNone(self):
        '''测试IOS参数缺失'''
        self.params['event_id'] = ""
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: event_id, error: event_id is required.")

    def test_getDeeplinkPicConfig_type(self):
        '''验证返回值是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getDeeplinkPicConfig_ios_type(self):
        '''验证IOS 返回值是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getDeeplinkPicConfig_picList_type(self):
        '''验证图片返回数据格式是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_getDeeplinkPicConfig_ios_picList_type(self):
        '''验证IOS 图片返回数据格式是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_getDeeplinkPicConfig_isPicKeyword(self):
        '''验证活动数据关键字是否齐全'''
        keylist = ["picId", "deeplinkPicAsset"]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                             keylist),
                        msg="活动关键字缺失")

    def test_getDeeplinkPicConfig_ios_isPicKeyword(self):
        '''验证IOS 活动数据关键字是否齐全'''
        keylist = ["picId", "deeplinkPicAsset"]
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                             keylist),
                        msg="活动关键字缺失")

    def test_getDeeplinkPicConfig_event_id(self):
        '''验证返回活动id是否于请求参数相同'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertEqual(result['data']['eventId'], self.params['event_id'])

    def test_getDeeplinkPicConfig_ios_event_id(self):
        '''验证IOS 返回活动id是否于请求参数相同'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertEqual(result['data']['eventId'], self.params['event_id'])

    def test_getDeeplinkPicConfig_isAssKeyword(self):
        '''验证活动资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(
            result['data']['picList'][0]['deeplinkPicAsset'], keylist),
                        msg="资源关键字缺失")

    def test_getDeeplinkPicConfig_ios_isAssKeyword(self):
        '''验证IOS 活动资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(
            result['data']['picList'][0]['deeplinkPicAsset'], keylist),
                        msg="资源关键字缺失")


if __name__ == '__main__':
    unittest.main()
