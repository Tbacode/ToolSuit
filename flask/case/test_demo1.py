'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-03-25 16:49:50
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-25 16:49:50
'''
import unittest


class A(unittest.TestCase):

    def test_a1(self):
        self.assertEqual(1, 1)

    def test_a2(self):
        self.assertEqual(2, 2)


class B(unittest.TestCase):

    def test_b1(self):
        self.assertEqual(1, 1)

    def test_b2(self):
        self.assertEqual(1, 1)