'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-07-19 17:09:30
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-07-19 18:14:10
'''
from unittest import mock
import unittest
from request import Request


class MockTest(unittest.TestCase):
    def setUp(self):
        print("case执行开始")

    def tearDown(self):
        print("case执行结束")

    def test_01(self):
        url = "http://www.baidu.com"
        parm = {"username": "了不起的QA"}

        req = Request()
        req.request_get = mock.Mock(return_value=200)
        request = req.request_get(url, parm)
        self.assertEqual(200, request)


if __name__ == "__main__":
    unittest.main()
