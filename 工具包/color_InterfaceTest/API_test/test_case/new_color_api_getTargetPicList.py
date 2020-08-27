'''
@Descripttion: 新color getTargetPicList接口APItest脚本
@Author: Tommy
@Date: 2020-07-17 11:49:37
LastEditors: Tommy
LastEditTime: 2020-08-27 11:24:56
'''
import unittest
import time
import json
from tool import Tool
# from unittest import TestSuite


class GetTargetPicList_new(unittest.TestCase):
    '''GetTargetPicList API 测试'''
    @classmethod
    def setUpClass(cls):
        with open("config.json", "r") as f:
            cls.value_dict = json.load(f)

    def setUp(self):
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.base_url = ''.join([
            self.__class__.value_dict['new_color_url'],
            'normalApi/v1/getTargetPicList'
        ])
        # self.url = 'https://tapcolor-lite.weplayer.cc/getBannerConfig?'
        # pic_list测试数据不能只有一个
        self.params = {"pic_list": "pic_EGbUVROpR,pic_pAWnmNx2l"}

    # def test_getNewsConfig_content(self):
    #     '''测试新老接口返回数值是否相同'''
    #     r1 = requests.get(self.url, params=self.params)
    #     result1 = r1.json()
    #     self.url = ''.join(
    #         [self.__class__.value_dict['url_new'], 'getTargetPicList_v1'])
    #     r2 = requests.get(self.url, params=self.params)
    #     result2 = r2.json()
    #     Tool.cmp(result2, result1, "picName")

    def test_new_getNewsConfig_success(self):
        '''测试新color getNewsConfig成功'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            self.__class__.value_dict['os_type'],
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertEqual(
            result['data']['picLength'],
            len(self.params['pic_list'].split(',')))  # 测试新color 数据不能为一个，否则报错

    def test_new_getNewsConfig_ios_success(self):
        '''测试新color IOS getNewsConfig成功'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            "Ios",
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertEqual(result['data']['picLength'],
                         len(self.params['pic_list'].split(',')))

    def test_new_getNewsConfig_dateError(self):
        '''测试新color 时间格式错误'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            self.__class__.value_dict['os_type'],
            self.__class__.value_dict['register_date'],
            "2020-08-25",
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_new_getNewsConfig_ios_dateError(self):
        '''测试新color IOS 时间格式错误'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            "Ios",
            self.__class__.value_dict['register_date'],
            "2020-08-25",
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(
            result['error_msg'],
            "path: game_date, error: game_date must have a length between 8 and 8."
        )

    def test_new_getNewsConfig_requestsError(self):
        '''测试新color requests错误'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            self.__class__.value_dict['os_type'],
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        self.params['pic_list'] = ""
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], 802)
        self.assertEqual(result['errorMsg'],
                         {'message': 'your requested data is empty, please check your picList'})

    def test_new_getNewsConfig_ios_requestsError(self):
        '''测试新color IOS requests错误'''
        self.params['pic_list'] = ""
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            "Ios",
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], 802)
        self.assertEqual(result['errorMsg'],
                         {'message': 'your requested data is empty, please check your picList'})

    def test_new_getNewsConfig_actDayNone(self):
        '''测试新color 参数缺失'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            self.__class__.value_dict['os_type'],
            self.__class__.value_dict['register_date'],
            self.game_date,
            "",
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_actDay, error: game_actDay is required.")

    def test_new_getNewsConfig_ios_actDayNone(self):
        '''测试新color IOS 参数缺失'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            "Ios",
            self.__class__.value_dict['register_date'],
            self.game_date,
            "",
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['error_code'], 666)
        self.assertEqual(result['error_msg'],
                         "path: game_actDay, error: game_actDay is required.")

    def test_new_getNewsConfig_type(self):
        '''验证新color 返回值是否正确'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            self.__class__.value_dict['os_type'],
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_new_getNewsConfig_ios_type(self):
        '''验证新color IOS 返回值是否正确'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            "Ios",
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertIsInstance(result, dict)

    def test_new_getNewsConfig_picList_type(self):
        '''验证新color 图片返回数据格式是否正确'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            self.__class__.value_dict['os_type'],
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_new_getNewsConfig_ios_picList_type(self):
        '''验证新color IOS 图片返回数据格式是否正确'''
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            "Ios",
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_type(result['data']['picList'], dict))

    def test_new_getNewsConfig_isPicKeyword(self):
        '''验证新color 图片数据关键字是否齐全'''
        keylist = [
            "picName", "picType", "picClass", "picUnlockDate",
            "picVipUnlockDate", "picExpireDate", "picUnlockType",
            "picUnlockNumber", "picJigsawId", "picAssets", "picOrder"
        ]
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            self.__class__.value_dict['os_type'],
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                             keylist),
                        msg="图片关键字缺失")

    def test_new_getNewsConfig_ios_isPicKeyword(self):
        '''验证新color IOS 图片数据关键字是否齐全'''
        keylist = [
            "picName", "picType", "picClass", "picUnlockDate",
            "picVipUnlockDate", "picExpireDate", "picUnlockType",
            "picUnlockNumber", "picJigsawId", "picAssets", "picOrder"
        ]
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            "Ios",
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword(result['data']['picList'],
                                             keylist),
                        msg="图片关键字缺失")

    def test_new_getNewsConfig_isAssKeyword(self):
        '''验证新color 图片资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            self.__class__.value_dict['os_type'],
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword_picAssets(
            result['data']['picList'], keylist),
                        msg="资源关键字缺失")

    def test_new_getNewsConfig_ios_isAssKeyword(self):
        '''验证新color IOS 图片资源关键字是否齐全'''
        keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
        self.url = "{}?game_ver={}&os_type={}&register_date={}&game_date={}&game_actDay={}".format(
            self.base_url,
            self.__class__.value_dict['game_ver'],
            "Ios",
            self.__class__.value_dict['register_date'],
            self.game_date,
            self.__class__.value_dict['game_actDay'],
        )
        result = Tool.request_post_result(self.url, self.params)
        # 断言
        self.assertEqual(result['errorCode'], -1)
        self.assertTrue(Tool.check_isKeyword_picAssets(
            result['data']['picList'], keylist),
                        msg="资源关键字缺失")


if __name__ == '__main__':
    unittest.main()
    # suite = TestSuite()
    # suite.addTest(GetTargetPicList_new('test_new_getNewsConfig_ios_requestsError'))
    # unittest.TextTestRunner().run(suite)
