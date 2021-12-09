'''
 * @Description  : ceshi
 * @Autor        : Tommy
 * @Date         : 2021-08-23 00:39:43
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-02 02:48:26
'''
import unittest
import requests


class RequestsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("设置url值")
        cls.url = "http://127.0.0.1:5000"
        cls.data = {"username": "了不起的QA", "password": 1234}

    def setUp(self):
        print("setUp执行")
        # self.url = "http://127.0.0.1:5000/get"

    # def test_request_username(self):
    #     print(self.test_request_username.__name__)  # 获取方法名

    #     self.assertEqual("了不起的QA", self.res["username"])

    # def test_request_password(self):
    #     print(self.test_request_password.__name__)
    #     self.assertEqual("11111", self.res["password"])

    def test_post_username(self):
        print(self.test_post_username.__name__)
        self.__class__.data["password"] = 1111
        res = requests.post(self.__class__.url, data=self.__class__.data).json()
        self.assertEqual("1234", res["password"])

    def test_post_username2(self):
        print(self.test_post_username2.__name__)
        res = requests.post(self.__class__.url, data=self.__class__.data).json()
        self.assertEqual("1234", res["password"])
    
    def tearDown(self):
        print("tearDown执行")
        self.__class__.data = {"username": "了不起的QA", "password": 1234}


if __name__ == "__main__":
    unittest.main()