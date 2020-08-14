# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2020-03-16 15:56:46
# @Last Modified by:   Tommy
# @Last Modified time: 2020-04-02 11:39:27
# import unittest


# def sum(a, b):
#     return a + b


# class MyTestCase(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         print("setUpClass")

#     def setUp(self):
#         print("setUp")

#     def test_case1(self):
#         self.assertEqual(sum(1, 2), 3)

#     def test_case2(self):
#         self.assertEqual(sum(1.1, 1.2), 2.3)

#     def tearDown(self):
#         print("tearDown")

#     @classmethod
#     def tearDownClass(cls):
#         print("tearDownClass")


# if __name__ == '__main__':
#     unittest.main()
import pytest


class Stack():

    # @pytest.mark.parametrize("input, expect", [
    #     (5, 6),
    #     (7, 8),
    #     (9, 10),
    #     (0, 1),
    #     (2, 2)])
    # @pytest.mark.fail
    # def test_case3(self, input, expect):
    #     print("test_case3")
    #     assert sum(input) == expect

    # @pytest.mark.success
    # def test_case4(self):
    #     print("test_case4")
    #     assert sum(4) == 5
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    def get_size(self):
        return len(self._data)


class TestStack():
    def setup(self):
        self.stack = Stack()

    @pytest.mark.parametrize("test_data", ["{}"])
    def test_match(self, test_data):
        '''堆栈测试'''
        assert self.match(test_data) == 0

    def match(self, data):
        for c in data:
            if c in "{[(":
                self.stack.push(c)
            elif c in "}])":
                self.stack.pop()
        return self.stack.get_size()


if __name__ == '__main__':
    pytest.main(
        [r"--html=.\reprot\report.html", "--self-contained-html"])
