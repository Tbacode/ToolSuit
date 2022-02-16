'''
 * @Descripttion : 引入ddt的主逻辑方法
 * @Author       : Tommy
 * @Date         : 2021-07-02 14:41:35
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-25 15:24:09
'''
from logging import exception
import ddt
import unittest
from Util.handle_excel import excel
from Base.base_request import request
# from Util.handle_ini import handle_ini
from Util.handle_result import handle_result
from Util.precondition_data import depend_data, get_depend_data, split_data_by_ExpectedResult, get_result_check
from Util.handle_email import handle_email
import time
import json
from loguru import logger
from BSTestRunner import BSTestRunner

data = excel.get_excel_data()


@ddt.ddt
class TestRunCaseDDT(unittest.TestCase):
    @ddt.data(*data)
    def test_run_main(self, data):
        Case_Id, \
            Description, \
            Is_Run, \
            Precondition, \
            Depend_key, \
            Url, \
            Method, \
            Data, \
            Expected_Method, \
            Expected_Result, \
            Execute_Result, \
            ResponseResult = data

        # 判断是否需要执行case
        if Is_Run == 'yes':
            # 获得index数据i，既：行号
            i = excel.get_row_number(Case_Id, 'A')

            # 判断是否有前置条件
            if Precondition:
                # 如果存在前置条件，及获取依赖字段的值
                cell_data, rule_data = depend_data(Precondition, 'A', 11)
                dependData = get_depend_data(cell_data, rule_data)
                logger.debug("依赖数据：" + dependData)
                # 替换掉依赖字段对应的依赖数据
                Data = eval(Data)
                # logger.debug("Data类型" + type(Data))
                Data[Depend_key] = dependData
                # logger.debug("Data数据" + Data)
                Data = json.dumps(Data)

            # 执行请求，获得返回结果
            if Data:
                request_data = json.loads(Data)
                if request_data['game_date'] == "":
                    time_str = time.strftime("%Y%m%d", time.localtime())
                    request_data['game_date'] = time_str
                Data = request_data

            res = request.run_main(Method, Url, Data)
            # 获取errorcode和errorMsg，存在两种字段，既需要分开处理
            try:
                result_code = res['errorCode']
            except KeyError:
                result_code = res['error_code']
            try:
                result_msg = res['errorMsg']
            except KeyError:
                try:
                    result_msg = res['error_msg']
                except KeyError:
                    result_msg = None
            # 判断预期结果验证方式
            if Expected_Method == "errorMsg":
                # 判断文件内errorMsg和返回值errorMsg是否一致
                message = handle_result('Config/check_config.json',
                                        result_code, "config")
                if type(message) is not list:
                    try:
                        self.assertEqual(message, result_msg)
                        excel.excel_write_data(i, 11, "PASS")
                        excel.excel_write_data(i, 12, str(res))
                    except Exception as e:
                        logger.error("接口失败errorMsg:" + str(result_msg))
                        excel.excel_write_data(i, 11, "FAIL")
                        excel.excel_write_data(i, 12, str(res))
                        raise e
                else:
                    for i_result_msg in message:
                        if i_result_msg == result_msg:
                            result = True
                            break
                        else:
                            result = False
                    try:
                        self.assertTrue(result, True)
                        excel.excel_write_data(i, 11, "PASS")
                        excel.excel_write_data(i, 12, str(res))
                    except Exception as e:
                        logger.error("接口失败errorMsg:" + str(result_msg))
                        excel.excel_write_data(i, 11, "FAIL")
                        excel.excel_write_data(i, 12, str(res))
                        raise e
            elif Expected_Method == "errorCode":
                # 判断errorCode返回值和预期结果返回值是否一致
                try:
                    self.assertEqual(Expected_Result, str(result_code))
                    excel.excel_write_data(i, 11, "PASS")
                    excel.excel_write_data(i, 12, str(res))
                except Exception as e:
                    logger.error("接口失败errorCode:" + str(result_msg))
                    excel.excel_write_data(i, 11, "FAIL")
                    excel.excel_write_data(i, 12, str(res))
                    raise e
            elif Expected_Method == "keyWords":
                # 判断关键字数值是否与预期一致
                rule_data_result, operator, expectedresult = split_data_by_ExpectedResult(Expected_Result)
                depend_data_result = get_depend_data(res, rule_data_result)
                result = get_result_check(depend_data_result, operator, expectedresult)
                try:
                    self.assertTrue(result)
                    excel.excel_write_data(i, 11, "PASS")
                    excel.excel_write_data(i, 12, str(depend_data_result))
                except Exception as e:
                    logger.error("接口预期结果{0}与实际结果{1}不符:".format(expectedresult, depend_data_result))
                    excel.excel_write_data(i, 11, "FAIL")
                    excel.excel_write_data(i, 12, str("接口预期结果{0}与实际结果{1}不符:".format(expectedresult, depend_data_result)))
                    raise e
                # excel.excel_write_data(i, 12, str(res))


if __name__ == "__main__":
    # unittest.main()
    case_path = r"../"
    report_path = r"..\color_interface.html"
    discover = unittest.defaultTestLoader.discover(case_path,
                                                   pattern="run_case_*.py")
    with open(report_path, 'wb') as f:
        runner = BSTestRunner(stream=f,
                              title="Color API Test Report",
                              description="Color API Test Report")
        test_result = runner.run(discover)
    if test_result.failure_count != 0:
        handle_email.post_file(report_path, True)
    elif test_result.error_count != 0:
        handle_email.post_file(report_path, True)
    else:
        # handle_email.post_file(report_path, True)
        pass
