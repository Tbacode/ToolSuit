'''
@Descripttion: getBannerConfig接口APItest脚本
@Author: Tommy
@Date: 2020-06-01 15:47:25
LastEditors: Tommy
LastEditTime: 2020-08-24 16:26:19
'''
import unittest
import time
import json
from tool import Tool


class GetBannerConfig_new(unittest.TestCase):
    '''GetBannerconfig API测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", 'r') as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.url = ''.join(
            [self.__class__.value_dict['new_color_url'], 'normalApi/v1/getBannerConfig'])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getBannerConfig?'
        self.params = {
            "game_ver": self.__class__.value_dict['game_ver'],
            "os_type": self.__class__.value_dict['os_type'],
            "register_date": self.__class__.value_dict['register_date'],
            "game_date": self.game_date,
            "game_actDay": self.__class__.value_dict['game_actDay']
        }

    def test_getBannerConfig_success(self):
        '''测试新color getBannerConfig接口成功'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['bannerList']), 0, msg="bannerlist数据为空")

    def test_getBannerConfig_ios_success(self):
        '''测试新color IOS getBannerConfig接口成功'''
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertNotEqual(len(result['data']['bannerList']), 0, msg="bannerlist数据为空")

    def test_getBannerConfig_requestsError(self):
        '''测试新color requests错误'''
        del self.params['game_date']
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_date, error: game_date is required.")

    def test_getBannerConfig_ios_requestsError(self):
        '''测试新color IOS requests错误'''
        del self.params['game_date']
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
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
        '''测试新color 日期格式错误'''
        self.params['game_date'] = "0"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getBannerConfig_ios_dateError(self):
        '''测试新color IOS 日期格式错误'''
        self.params['game_date'] = "0"
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_getBannerConfig_type(self):
        '''验证新color 返回值格式是否正确'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getBannerConfig_ios_type(self):
        '''验证新color IOS 返回值格式是否正确'''
        self.params['os_type'] = "Ios"
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_getBannerConfig_listType(self):
        '''验证新color bannerList下是否格式正确'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['bannerList'], dict),
                        msg='子项格式错误')

    def test_getBannerConfig_ios_listType(self):
        '''验证新color IOS bannerList下是否格式正确'''
        result = Tool.request_get_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['bannerList'], dict),
                        msg='子项格式错误')


if __name__ == '__main__':
    unittest.main()
