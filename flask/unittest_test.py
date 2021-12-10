'''
 * @Description  : ceshi
 * @Autor        : Tommy
 * @Date         : 2021-08-23 00:39:43
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-10 11:52:27
'''
import unittest
import requests


class RequestsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = r"http://127.0.0.1:5000/"

    def setUp(self) -> None:
        self.data = {"username": "了不起的QA", "password": 123456}

    def test_login_success(self):
        url = ''.join([self.__class__.url, "login"])
        res = requests.post(url=url, data=self.data).json()
        self.assertEqual(200, res['errorCode'])

    def test_login_fail(self):
        self.data['username'] = "手动阀手动阀"
        url = ''.join([self.__class__.url, "login"])
        res = requests.post(url=url, data=self.data).json()
        self.assertEqual(301, res['errorCode'])

    def test_userinfo_success(self):
        url = ''.join([self.__class__.url, "userinfo"])
        res = requests.get(url=url, params=self.data).json()
        self.assertEqual(200, res['errorCode'])

    def test_userinfo_fail(self):
        self.data['username'] = None
        url = ''.join([self.__class__.url, "userinfo"])
        res = requests.get(url=url, params=self.data).json()
        self.assertEqual(301, res['errorCode'])


if __name__ == "__main__":
    unittest.main()
