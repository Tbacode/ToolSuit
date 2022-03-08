'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-13 18:31:10
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-02-21 14:33:09
'''
import unittest


class TestLogin(unittest.TestCase):

    def condition():
        return True

    def setUp(self) -> None:
        print("*" * 20)
        print("Login接口测试-setup")

    def test_login_success(self):
        print("test_login_success测试开始")

    @unittest.skip('tiaoguo')
    def test_login_fail(self):
        print("test_login_fail测试开始")

    def tearDown(self) -> None:
        print("Login接口测试-tearDown")
        print("*" * 20)


if __name__ == "__main__":
    unittest.main()
