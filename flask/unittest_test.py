'''
 * @Description  : ceshi
 * @Autor        : Tommy
 * @Date         : 2021-08-23 00:39:43
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-09-02 01:46:51
'''
import unittest
import requests


class RequestsTest(unittest.TestCase):
    def test_request_username(self):
        url = "http://127.0.0.1:5000/get"
        res = requests.get(url).json()
        self.assertEqual("了不起的QA", res["username"])


if __name__ == "__main__":
    unittest.main()