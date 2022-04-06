'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-13 18:31:10
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-11 16:57:13
'''
import unittest


class TestUserinfo(unittest.TestCase):

    def setUp(self) -> None:
        print("userinfo接口测试-setup")

    # @unittest.skip("强制跳过")
    def test_userinfo_success(self):
        print("test_userinfo_success测试开始")
        print(self._outcome.result.failures)

    # @unittest.skipIf(3>2, "skipIf条件为真跳过")
    def test_userinfo_fail(self):
        print("test_userinfo_fail测试开始")
        assert False

    @unittest.skipUnless(3<2, "skipUnless条件为假跳过")
    def test_userinfo_error(self):
        print("test_userinfo_error测试开始")

    def tearDown(self) -> None:
        print("userinfo接口测试-tearDown")


if __name__ == "__main__":
    unittest.main(verbosity=2)
