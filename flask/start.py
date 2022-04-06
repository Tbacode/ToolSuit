'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-03-25 16:52:40
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-28 14:21:30
'''
import unittest
from BSTestRunner import BSTestRunner


# CASE_PATH = r'./case'

# # 测试套件
# suit = unittest.TestSuite()

# # 测试加载器
# loader = unittest.defaultTestLoader

# test_suit = loader.discover(CASE_PATH, pattern='test*.py')

# suit.addTest(test_suit)

# # 测试执行器

# runner = unittest.TextTestRunner()
# runner.run(suit)


case_path = r"./case"
report_path = r".\reports\color_interface.html"
discover = unittest.defaultTestLoader.discover(case_path,
                                               pattern="test*.py")
with open(report_path, 'wb') as f:
    runner = BSTestRunner(stream=f,
                          title="报告标题",
                          description="报告描述")
    test_result = runner.run(discover)
