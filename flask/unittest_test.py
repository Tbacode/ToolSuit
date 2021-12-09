'''
 * @Description  : ceshi
 * @Autor        : Tommy
 * @Date         : 2021-08-23 00:39:43
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-07 19:01:38
'''
from _typeshed import Self
import unittest
import requests


class RequestsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = r"http://127.0.0.1:5000"

    def setUp(self) -> None:
        self.data = {"username": "了不起的QA", "password": 123456}

    def test_login_success(self):
        res = requests.post(url=self.__class__.url, data=self.data)
        self.assertEqual(200, res['errorCode'])

    def test_login_fail(self):
        self.data['username'] = "手动阀手动阀"
        res = requests.post(url=self.__class__.url, data=self.data)
        self.assertEqual(301, res['errorCode'])

if __name__ == "__main__":
    unittest.main()
