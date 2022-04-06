'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-03-25 16:49:58
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-28 14:44:21
'''
import unittest


class C(unittest.TestCase):

    def test_c1(self):
        self.assertEqual(1, 1)

    def test_c2(self):
        self.assertEqual(2, 3)


class D(unittest.TestCase):

    def test_d1(self):
        self.assertEqual(1, 1)

    def test_d2(self):
        self.assertEqual(1, 1)
