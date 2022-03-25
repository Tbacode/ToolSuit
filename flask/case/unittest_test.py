'''
 * @Description  : ceshi
 * @Autor        : Tommy
 * @Date         : 2021-08-23 00:39:43
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-24 18:35:54
'''
import unittest
import paramunittest
import requests


# @paramunittest.parametrized(
#     ('了不起的QA', '123456', 200),
#     ('手动阀手动阀', '123456', 200)
# )
# class RequestsTest(unittest.TestCase):

#     def setParameters(self, name, password, ass):
#         self.name = name
#         self.password = password
#         self.ass = ass

#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.url = r"http://127.0.0.1:5000/"

#     def setUp(self) -> None:
#         self.data = {"username": self.name, "password": self.password}

#     def test_login(self):
#         url = ''.join([self.__class__.url, "login"])
#         # data = {"username": self.name, "password": self.password}
#         res = requests.post(url=url, data=self.data).json()
#         self.assertEqual(self.ass, res['errorCode'])


data = (
    {'username': '了不起的QA', 'password': 123456, 'ass': 200},
    {'username': '手动阀手动阀', 'password': 123456, 'ass': 200}
)


class TestDemo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.url = r"http://127.0.0.1:5000/"

    def test_login(self):
        for d in data:
            with self.subTest(d):
                url = ''.join([self.__class__.url, "login"])
                res = requests.post(url=url, data=d).json()
                self.assertEqual(d['ass'], res['errorCode'])

    # def test_login_success(self):
    #     url = ''.join([self.__class__.url, "login"])
    #     res = requests.post(url=url, data=self.data).json()
    #     self.assertEqual(200, res['errorCode'])

    # def test_login_fail(self):
    #     self.data['username'] = "手动阀手动阀"
    #     url = ''.join([self.__class__.url, "login"])
    #     res = requests.post(url=url, data=self.data).json()
    #     self.assertEqual(301, res['errorCode'])

    # def test_userinfo_success(self):
    #     url = ''.join([self.__class__.url, "userinfo"])
    #     res = requests.get(url=url, params=self.data).json()
    #     self.assertEqual(200, res['errorCode'])

    # def test_userinfo_fail(self):
    #     self.data['username'] = None
    #     url = ''.join([self.__class__.url, "userinfo"])
    #     res = requests.get(url=url, params=self.data).json()
    #     self.assertEqual(301, res['errorCode'])


if __name__ == "__main__":
    unittest.main(verbosity=1)
