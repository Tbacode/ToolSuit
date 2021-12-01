'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-09-03 17:38:30
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-10-04 21:08:15
'''
import unittest


class UnittestTest(unittest.TestCase):

    def test_01(self):
        flag = True
        self.assertTrue(flag)

    def test_02(self):
        flag = False
        self.assertFalse(flag)

    def test_03(self):
        flag1 = 1
        flag2 = 2
        self.assertEqual(flag1, flag2)

    def test_04(self):
        data1 = {"username": "了不起的QA", "password": "123"}
        data2 = {"username": "了不起的GD", "password": "1234"}
        self.assertDictEqual(data1, data2)

    def test_05(self):
        data1 = {"username": "了不起的QA", "password": "123"}
        self.assertIsInstance(data1, str)


if __name__ == "__main__":
    unittest.main()
