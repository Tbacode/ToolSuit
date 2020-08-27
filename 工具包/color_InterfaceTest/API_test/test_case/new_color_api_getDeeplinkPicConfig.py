'''
@Descripttion: 新color getDeeplinkPicConfig接口APItest脚本
@Author: Tommy
@Date: 2020-07-17 11:35:59
LastEditors: Tommy
LastEditTime: 2020-08-24 18:54:54
'''
import unittest
import time
import json
import random
from tool import Tool


class GetDeeplinkPicConfig_new(unittest.TestCase):
    '''GetDeeplinkPicConfig API 测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)
        cls.event_list = Tool.request_get_result(
            cls.value_dict['new_color_event_url'], None)

    def setUp(self):
        event_index = random.randint(0, len(self.__class__.event_list) - 1)
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join([
            self.__class__.value_dict['new_color_url'],
            'normalApi/v1/getDeeplinkPicConfig'
        ])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getBannerConfig?'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay'],
            # "event_id": "8CN0wZVC5o",
            "event_id": self.__class__.event_list[event_index]['event_id']
        }

    # def test_new_getDeeplinkPicConfig_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getDeeplinkPicConfig_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, "picId")
    #     print(result2)

    def test_new_getDeeplinkPicConfig_dateError(self):
        '''测试新color 日期格式错误'''
        self.params['game_date'] = "2020-05-29"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'],
                         666,
                         msg="event_id = {}".format(self.params['event_id']))
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_new_getDeeplinkPicConfig_ios_dateError(self):
        '''测试新color IOS 日期格式错误'''
        self.params['game_date'] = "2020-05-29"
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'],
                         666,
                         msg="event_id = {}".format(self.params['event_id']))
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_new_getDeeplinkPicConfig_requestsError(self):
        '''测试新color requests错误'''
        del self.params['event_id']
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: event_id, error: event_id is required.")

    def test_new_getDeeplinkPicConfig_ios_requestsError(self):
        '''测试新color IOS requests错误'''
        del self.params['event_id']
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: event_id, error: event_id is required.")

    def test_new_getDeeplinkPicConfig_eventNone(self):
        '''测试新color 参数缺失'''
        self.params['event_id'] = ""
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'],
                         666,
                         msg="event_id = {}".format(self.params['event_id']))
        self.assertEqual(result['error_msg'],
                         "path: event_id, error: event_id is required.")

    def test_new_getDeeplinkPicConfig_ios_eventNone(self):
        '''测试新color IOS参数缺失'''
        self.params['event_id'] = ""
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'],
                         666,
                         msg="event_id = {}".format(self.params['event_id']))
        self.assertEqual(result['error_msg'],
                         "path: event_id, error: event_id is required.")

    def test_new_getDeeplinkPicConfig_type(self):
        '''验证新color 返回值是否正确'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        self.assertIsInstance(result, dict)

    def test_new_getDeeplinkPicConfig_ios_type(self):
        '''验证新color IOS 返回值是否正确'''
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        self.assertIsInstance(result, dict)

    def test_new_getDeeplinkPicConfig_picList_type(self):
        '''验证新color 图片返回数据格式是否正确'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        if result['data']['eventType'] != "feature":
            self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_new_getDeeplinkPicConfig_ios_picList_type(self):
        '''验证新color IOS 图片返回数据格式是否正确'''
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        if result['data']['eventType'] != "feature":
            self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_new_getDeeplinkPicConfig_isPicKeyword(self):
        '''验证新color 活动数据关键字是否齐全'''
        keylist = ["picId", "deeplinkPicAsset"]
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        if result['data']['eventType'] != "feature":
            self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                                 keylist),
                            msg="活动关键字缺失")

    def test_new_getDeeplinkPicConfig_ios_isPicKeyword(self):
        '''验证新color IOS 活动数据关键字是否齐全'''
        keylist = ["picId", "deeplinkPicAsset"]
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        if result['data']['eventType'] != "feature":
            self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                                 keylist),
                            msg="活动关键字缺失")

    def test_new_getDeeplinkPicConfig_event_id(self):
        '''验证新color 返回活动id是否于请求参数相同'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        self.assertEqual(result['data']['eventId'], self.params['event_id'])

    def test_new_getDeeplinkPicConfig_ios_event_id(self):
        '''验证新color IOS 返回活动id是否于请求参数相同'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        self.assertEqual(result['data']['eventId'], self.params['event_id'])

    def test_new_getDeeplinkPicConfig_isAssKeyword(self):
        '''验证新color 活动资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        if result['data']['eventType'] != "feature":
            self.assertTrue(Tool.check_isKeyword(
                result['data']['picList'][0]['deeplinkPicAsset'], keylist),
                            msg="资源关键字缺失")

    def test_new_getDeeplinkPicConfig_ios_isAssKeyword(self):
        '''验证新color IOS 活动资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'],
                         -1,
                         msg="event_id = {}".format(self.params['event_id']))
        if result['data']['eventType'] != "feature":
            self.assertTrue(Tool.check_isKeyword(
                result['data']['picList'][0]['deeplinkPicAsset'], keylist),
                            msg="资源关键字缺失")


if __name__ == '__main__':
    unittest.main()
