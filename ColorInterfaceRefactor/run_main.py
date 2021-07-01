'''
 * @Descripttion : Main函数
 * @Author       : Tommy
 * @Date         : 2021-06-17 15:13:38
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-07-01 19:59:10
'''
# import json
from Util.handle_excel import excel
from Base.base_request import request
from Util.handle_ini import handle_ini
from Util.handle_result import handle_result
from Util.precondition_data import depend_data, get_depend_data
import time
import json
from loguru import logger


class RunMain(object):
    def init_excel_index(self):
        '''
         * @name: Tommy
         * @msg: 打开ini文件获取case索引值
         * @param {*}
         * @return {返回各列索引值}
        '''
        Is_Run_index = int(handle_ini.get_ini_value("Is_Run"))
        Precondition_index = int(handle_ini.get_ini_value("Precondition"))
        Url_index = int(handle_ini.get_ini_value("Url"))
        Method_index = int(handle_ini.get_ini_value("Method"))
        Data_index = int(handle_ini.get_ini_value("Data"))
        Expected_Method_index = int(
            handle_ini.get_ini_value("Expected_Method"))
        Expected_Result_index = int(
            handle_ini.get_ini_value("Expected_Result"))
        Execute_Result_index = int(handle_ini.get_ini_value("ExecuteResult"))
        ResponseResult_index = int(handle_ini.get_ini_value("ResponseResult"))
        return Is_Run_index, \
            Precondition_index, \
            Url_index, \
            Method_index, \
            Data_index, \
            Expected_Method_index, \
            Expected_Result_index, \
            Execute_Result_index, \
            ResponseResult_index

    def run_case(self):
        rows = excel.get_rows()
        Is_Run_index, \
            Precondition_index, \
            Url_index, \
            Method_index, \
            Data_index, \
            Expected_Method_index, \
            Expected_Result_index, \
            Execute_Result_index, \
            ResponseResult_index = self.init_excel_index()
        for i in range(rows):
            data = excel.get_rows_value(i + 2)
            is_run = data[Is_Run_index]
            # 判断是否需要执行case
            if is_run == 'yes':

                # 判断是否有前置条件
                if data[Precondition_index]:
                    # 如果存在前置条件，及获取依赖字段的值
                    cell_data, rule_data = depend_data(
                        data[Precondition_index], 'A', ResponseResult_index)
                    print(cell_data)
                    print(type(cell_data))
                    print(rule_data)
                    dependData = get_depend_data(cell_data, rule_data)
                    logger.debug("依赖数据：", dependData)
                    data = eval(data[Data_index].format("1", dependData))

                # 执行请求，获得返回结果
                time_str = time.strftime("%Y%m%d", time.localtime())
                if data[Data_index]:
                    request_data = json.loads(data[Data_index])
                    if request_data['game_date'] == "":
                        request_data['game_date'] = time_str
                    data[Data_index] = request_data

                res = request.run_main(
                    data[Method_index],
                    data[Url_index],
                    data[Data_index])
                # 获取errorcode和errorMsg，存在两种字段，既需要分开处理
                try:
                    result_code = res['errorCode']
                except KeyError:
                    result_code = res['error_code']
                try:
                    result_msg = res['errorMsg']
                except KeyError:
                    result_msg = res['error_msg']
                # 判断预期结果验证方式
                if data[Expected_Method_index] == "errorMsg":
                    # 判断文件内errorMsg和返回值errorMsg是否一致
                    message = handle_result('Config/check_config.json',
                                            result_code,
                                            "config")
                    if type(message) is not list:
                        if message == str(result_msg):
                            logger.debug("测试通过---")
                            excel.excel_write_data(i + 2,
                                                   Execute_Result_index + 1,
                                                   "通过")
                            excel.excel_write_data(i + 2,
                                                   ResponseResult_index + 1,
                                                   str(res))
                        else:
                            logger.debug("测试失败---")
                            excel.excel_write_data(i + 2,
                                                   Execute_Result_index + 1,
                                                   "失败")
                            excel.excel_write_data(i + 2,
                                                   ResponseResult_index + 1,
                                                   str(res))
                    else:
                        for i_result_msg in message:
                            if i_result_msg == result_msg:
                                result = "通过"
                                break
                            else:
                                result = "失败"
                        excel.excel_write_data(i + 2, Execute_Result_index + 1,
                                               result)
                        excel.excel_write_data(i + 2, ResponseResult_index + 1,
                                               str(res))
                        logger.debug(result)
                elif data[Expected_Method_index] == "errorCode":
                    # 判断errorCode返回值和预期结果返回值是否一致
                    if data[Expected_Result_index] == str(result_code):
                        logger.debug("测试通过---")
                        excel.excel_write_data(i + 2, Execute_Result_index + 1,
                                               "通过")
                        excel.excel_write_data(i + 2, ResponseResult_index + 1,
                                               str(res))
                    else:
                        logger.debug("测试失败---")
                        excel.excel_write_data(i + 2, Execute_Result_index + 1,
                                               "失败")
                        excel.excel_write_data(i + 2, ResponseResult_index + 1,
                                               str(res))
                else:
                    # 判断返回值是否json格式
                    excel.excel_write_data(i + 2, ResponseResult_index + 1,
                                           str(res))

                # with open('code_config.json', 'w', encoding='utf-8') as f:
                #     res = json.dumps(res)
                #     f.write(res)
                logger.debug("-" * 100)
                logger.debug(res)
                logger.debug("-" * 100)


if __name__ == "__main__":
    run = RunMain()
    run.run_case()
