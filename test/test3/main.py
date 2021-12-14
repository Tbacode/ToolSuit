'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-13 18:48:21
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-14 14:58:12
'''
import unittest

case_path = r'C:\Users\talefun\Documents\ToolSuit\test\test3'

discover = unittest.defaultTestLoader.discover(case_path, pattern="test_*.py", top_level_dir=None)
runner = unittest.TextTestRunner()
runner.run(discover)