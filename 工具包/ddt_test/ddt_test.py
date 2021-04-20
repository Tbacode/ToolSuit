'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-04-20 17:53:12
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-04-20 19:15:00
'''
import ddt
import unittest
from handle_excel import HandleExcel

path = "aa.xlsx"
excel_operation = HandleExcel(path)


data = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8],
        [5, 6, 7, 8, 9]]


@ddt.ddt
class TestCase01(unittest.TestCase):
    def setUp(self):
        print("case 执行开始")

    def tearDown(self):
        print("case 执行结束")

    @ddt.data(*data)
    def test_001(self, case_data):
        param1, param2, param3, param4, param5 = case_data
        print("this is test case", param1, param2, param3, param4, param5)


if __name__ == "__main__":
    print(excel_operation.get_table_by_index())
    unittest.main()
    