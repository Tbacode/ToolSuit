'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-03-25 16:52:40
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-25 17:15:36
'''
import unittest


CASE_PATH = r'./case'

# 测试套件
suit = unittest.TestSuite()

# 测试加载器
loader = unittest.defaultTestLoader

test_suit = loader.discover(CASE_PATH, pattern='test*.py')

suit.addTest(test_suit)

# 测试执行器

runner = unittest.TextTestRunner()
runner.run(suit)
