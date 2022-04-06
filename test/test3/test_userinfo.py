'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-13 18:31:19
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-10 16:15:01
'''
from functools import wraps
import unittest


def depend(depend=''):
    print("进入")
    _mark = []

    def wrap_func(func):
        @wraps(func)
        def inner_func(*args, **kwargs):
            if depend == func.__name__:
                print("cuowu")
            _r = args[0]._outcome.result
            _f, _e, _s = _r.failures, _r.errors, _r.skipped

            if not (_f or _e or _s):
                print("没有失败结果")
                func(*args, **kwargs)

            else:
                if _f:
                    _mark.extend([fail[0] for fail in _f])
                if _e:
                    _mark.extend([error[0] for error in _e])
                if _s:
                    _mark.extend([skip[0] for skip in _s])

                if depend in str(_mark):
                    unittest.skipIf(True, "跳过")(func)(*args, **kwargs)
                else:
                    func(*args, **kwargs)

        #     unittest.skipIf(
        #         depend in str(_mark),
        #         "跳过"
        #     )(func)(self)
        return inner_func
    return wrap_func


class TestUserinfo(unittest.TestCase):

    def setUp(self) -> None:
        print("userinfo接口测试-setup")

    @depend('test_userinfo_fail')
    def test_userinfo_success(self):
        print("test_userinfo_success测试开始")
        self.assertEqual(1, 1)

    def test_userinfo_fail(self):
        print("test_userinfo_fail测试开始")
        self.assertEqual(1, 3)

    def tearDown(self) -> None:
        print("userinfo接口测试-tearDown")


# @depend('test_userinfo_fail')
class Testtest(unittest.TestCase):

    @depend('test_userinfo_fail')
    def test_t(self):
        print("test_t测试开始")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    # suit = unittest.TestSuite()
    # suit.addTest(TestUserinfo("test_userinfo_success"))
    # suit.addTest(TestUserinfo("test_userinfo_fail"))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
    # print(r.failures)
