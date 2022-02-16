'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-13 18:31:19
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-02-16 18:40:34
'''
import unittest


class TestUserinfo(unittest.TestCase):

    def setUp(self) -> None:
        print("userinfo接口测试-setup")

    def test_userinfo_success(self):
        print("test_userinfo_success测试开始")

    def test_userinfo_fail(self):
        print("test_userinfo_fail测试开始")

    def tearDown(self) -> None:
        print("userinfo接口测试-tearDown")


if __name__ == "__main__":
    # unittest.main()
    suit = unittest.TestSuite()
    suit.addTest(TestUserinfo("test_userinfo_success"))
    runner = unittest.TextTestRunner()
    runner.run(suit)
