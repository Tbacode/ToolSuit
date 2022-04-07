'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-13 18:31:19
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-04-06 20:04:05
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
    # suit = unittest.TestSuite()
    # suit.addTest(TestUserinfo("test_userinfo_success"))
    # suit.addTest(TestUserinfo("test_userinfo_fail"))

    # cases = [
    #     TestUserinfo("test_userinfo_success"),
    #     TestUserinfo("test_userinfo_fail")
    # ]
    # suit.addTests(cases)
    suit = unittest.TestSuite(
        map(TestUserinfo, ["test_userinfo_success", "test_userinfo_fail"]))
    runner = unittest.TextTestRunner()
    runner.run(suit)
