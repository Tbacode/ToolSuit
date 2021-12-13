'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-13 18:31:10
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-13 18:42:27
'''
import unittest


class TestLogin(unittest.TestCase):

    def setUp(self) -> None:
        print("Login接口测试-setup")

    def test_login_success(self):
        print("test_login_success测试开始")

    def test_login_fail(self):
        print("test_login_fail测试开始")

    def tearDown(self) -> None:
        print("Login接口测试-tearDown")


if __name__ == "__main__":
    unittest.main()