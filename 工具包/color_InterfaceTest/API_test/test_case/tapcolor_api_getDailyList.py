'''
@Descripttion: getDaily接口APItest脚本
@Author: Tommy
@Date: 2020-05-29 17:53:26
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-04 15:32:47
'''
import unittest
import requests
import time
import json
import datetime
from tool import Tool


class GetDailyList(unittest.TestCase):
    """DailyList API测试"""
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.start_date = time.strftime("%Y%m%d", time.localtime())
        self.end_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join(
            [self.__class__.value_dict['url'], 'getDailyList_v1'])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getDailyList?'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay'],
            "start_date": self.start_date,
            "end_date": self.end_date
        }

    def test_daily_success(self):
        '''测试daily成功'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['data']['picLength'], 1)
        self.assertEqual(result['errorCode'], -1)

    def test_daily_ios_success(self):
        '''测试IOS daily成功'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['data']['picLength'], 1)
        self.assertEqual(result['errorCode'], -1)

    def test_daily_enddateError(self):
        '''测试结束日期大于开始日期'''
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        n_days = now + delta
        self.params['end_date'] = n_days.strftime('%Y%m%d')
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertEqual(len(result['data']['picList']), 0)

    def test_daily_ios_enddateError(self):
        '''测试IOS结束日期大于开始日期'''
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        n_days = now + delta
        self.params['end_date'] = n_days.strftime('%Y%m%d')
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertEqual(len(result['data']['picList']), 0)

    def test_daily_requestsError(self):
        '''测试requests错误'''
        del self.params['end_date']
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: end_date, error: end_date is required.")

    def test_daily_ios_requestsError(self):
        '''测试IOS requests错误'''
        del self.params['end_date']
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: end_date, error: end_date is required.")

    def test_daily_dateError(self):
        '''测试日期格式错误'''
        self.params['start_date'] = "2020-05-29"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: start_date, error: start_date must have a length between 8 and 8."
        )

    def test_daily_ios_dateError(self):
        '''测试IOS 日期格式错误'''
        self.params['start_date'] = "2020-05-29"
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: start_date, error: start_date must have a length between 8 and 8."
        )

    def test_daily_dateNone(self):
        '''测试参数缺失'''
        self.params['start_date'] = ""
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: start_date, error: start_date is required.")

    def test_daily_ios_dateNone(self):
        '''测试IOS 参数缺失'''
        self.params['start_date'] = ""
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: start_date, error: start_date is required.")

    # def test_daily_new_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     self.params['start_date'] = "20200715"
    #     self.params['end_date'] = "20200630"
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getDailyList_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool().cmp(result2, result1, "picName")

    def test_daily_type(self):
        '''验证返回值是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_daily_ios_type(self):
        '''验证IOS 返回值是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_daily_picList_type(self):
        '''验证图片返回数据格式是否正确'''
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool().check_type(result['data']['picList'], dict))

    def test_daily_ios_picList_type(self):
        '''验证IOS 图片返回数据格式是否正确'''
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool().check_type(result['data']['picList'], dict))

    def test_daily_isPicKeyword(self):
        '''验证图片数据关键字是否齐全'''
        keylist = [
            "picName", "picType", "picUnlockDate", "picExpireDate", "picAssets"
        ]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool().check_isKeyword(result['data']['picList'],
                                               keylist),
                        msg="图片关键字缺失")

    def test_daily_ios_isPicKeyword(self):
        '''验证IOS 图片数据关键字是否齐全'''
        keylist = [
            "picName", "picType", "picUnlockDate", "picExpireDate", "picAssets"
        ]
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool().check_isKeyword(result['data']['picList'],
                                               keylist),
                        msg="图片关键字缺失")

    def test_daily_isAssKeyword(self):
        '''验证图片资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool().check_isKeyword_picAssets(
            result['data']['picList'], keylist),
            msg="资源关键字缺失")

    def test_daily_ios_isAssKeyword(self):
        '''验证IOS 图片资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        self.params['os_type'] = "Ios"
        r = requests.get(self.url, params=self.params)
        result = r.json()
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool().check_isKeyword_picAssets(
            result['data']['picList'], keylist),
            msg="资源关键字缺失")


if __name__ == '__main__':
    unittest.main()
