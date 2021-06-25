'''
 * @Descripttion : Main函数
 * @Author       : Tommy
 * @Date         : 2021-06-17 15:13:38
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-24 14:31:11
'''
from Util.handle_excel import excel
from Base.base_request import request
from Util.handle_ini import handle_ini
import time


class RunMain(object):
    def init_excel_index(self):
        Is_Run_index = int(handle_ini.get_ini_value("Is_Run"))
        Precondition_index = int(handle_ini.get_ini_value("Precondition"))
        Url_index = int(handle_ini.get_ini_value("Url"))
        Method_index = int(handle_ini.get_ini_value("Method"))
        Data_index = int(handle_ini.get_ini_value("Data"))
        Expected_Result_index = int(
            handle_ini.get_ini_value("Expected_Result"))
        return Is_Run_index, Precondition_index, Url_index, Method_index, Data_index, Expected_Result_index

    def run_case(self):
        rows = excel.get_rows()
        Is_Run_index, Precondition_index, Url_index, Method_index, Data_index, Expected_Result_index = self.init_excel_index()
        for i in range(rows):
            data = excel.get_rows_value(i + 2)
            is_run = data[Is_Run_index]
            if is_run == 'yes':
                # TODO: 继续执行后续

                res = request.run_main(
                    data[Method_index], data[Url_index],
                    eval(data[Data_index].format(
                        time.strftime("%Y%m%d", time.localtime()))),
                    'colorhost')
                print("-" * 20)
                print(res)
                print("-" * 20)


if __name__ == "__main__":
    run = RunMain()
    run.run_case()
