'''
 * @Descripttion : ddt
 * @Author       : Tommy
 * @Date         : 2021-04-20 17:53:12
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-04-22 17:55:26
'''
import unittest
import ddt
from handle_excel import HandleExcel

path = "aa.xlsx"
excel_operation = HandleExcel(path)
data1 = excel_operation.get_excel_data()
print(data1)


@ddt.ddt
class TestCase01(unittest.TestCase):
    def setUp(self):
        print("case 执行开始")

    def tearDown(self):
        print("case 执行结束")

    @ddt.data(*data1)
    def test_001(self, case_data):
        case_id, case_description, api_url, post_method, param, check_code, check_param = case_data
        print("@@@@@", case_id, case_description, api_url, post_method, param,
              check_code, check_param)

    @ddt.data(*data1)
    @ddt.unpack
    def test_002(self, case_id, case_description, api_url, post_method, param,
                 check_code, check_param):
        case_id, case_description, api_url, post_method, param, check_code, check_param = case_id, case_description, api_url, post_method, param, check_code, check_param
        print("this is test case UNPACK", case_id, case_description, api_url,
              post_method, param, check_code, check_param)


if __name__ == "__main__":
    unittest.main()
