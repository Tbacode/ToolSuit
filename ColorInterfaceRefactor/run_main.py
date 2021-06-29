'''
 * @Descripttion : Main函数
 * @Author       : Tommy
 * @Date         : 2021-06-17 15:13:38
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-29 19:23:20
'''
# import json
from Util.handle_excel import excel
from Base.base_request import request
from Util.handle_ini import handle_ini
from Util.handle_result import handle_result
import time


class RunMain(object):
    def init_excel_index(self):
        Is_Run_index = int(handle_ini.get_ini_value("Is_Run"))
        Precondition_index = int(handle_ini.get_ini_value("Precondition"))
        Url_index = int(handle_ini.get_ini_value("Url"))
        Method_index = int(handle_ini.get_ini_value("Method"))
        Data_index = int(handle_ini.get_ini_value("Data"))
        Expected_Method_index = int(
            handle_ini.get_ini_value("Expected_Method"))
        Expected_Result_index = int(
            handle_ini.get_ini_value("Expected_Result"))
        return Is_Run_index, Precondition_index, Url_index, Method_index, Data_index, Expected_Method_index, Expected_Result_index

    def run_case(self):
        rows = excel.get_rows()
        Is_Run_index, Precondition_index, Url_index, Method_index, Data_index, Expected_Method_index, Expected_Result_index = self.init_excel_index(
        )
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
                try:
                    result_code = res['errorCode']
                except KeyError:
                    result_code = res['error_code']
                try:
                    result_msg = res['errorMsg']
                except KeyError:
                    result_msg = res['error_msg']
                message = handle_result(data[Url_index],
                                        'Config/check_config.json',
                                        result_code)
                if type(message) is not list:
                    if message == str(result_msg):
                        print("测试通过---")
                    else:
                        print("测试失败---")
                else:
                    for i_result_msg in message:
                        if i_result_msg == result_msg:
                            print("测试通过---")
                    print("测试失败---")
                # with open('code_config.json', 'w', encoding='utf-8') as f:
                #     res = json.dumps(res)
                #     f.write(res)
                print("-" * 100)
                print(res)
                print("-" * 100)


if __name__ == "__main__":
    run = RunMain()
    run.run_case()
