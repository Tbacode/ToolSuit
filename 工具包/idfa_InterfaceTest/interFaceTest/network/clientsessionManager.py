# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-06-26 14:49:57
# @Last Modified by:   Tommy
# @Last Modified time: 2019-11-06 16:57:54
from interFaceTest.network import handler_methods
import xlrd
import json
import xlwt


class ClientSessionManager(handler_methods.HandlerMethods):
    """
    客户端事件管理
    """
    __slots__ = ["action_dict", "count", "index"]
    casefile_rows = 0

    def __init__(self):
        self.action_dict = {}
        self.index = 0
        self.casefile = "interFaceTest/testcase/case.xls"
        self.sheetname = "测试用例"

    def add_session(self, keys: int, taskfd):
        self.action_dict[keys] = taskfd
        self.index += 1
        if taskfd:
            return True

    def get_session_length(self):
        """获取事务列表长度"""
        return len(self.action_dict)

    def get_file_rows(self):
        testcase = xlrd.open_workbook(self.casefile)
        st = testcase.sheet_by_index(0)
        setattr(ClientSessionManager, "casefile_rows", st.nrows)

    def get_testCase_info(self, testcase_file: str, caseId: int):
        """
        获得用例信息
        :param case_id: 用例名称
        :param description: 用例描述
        :param url: 用例链接
        :param method: 发送方法
        :param req_data: 发送数据
        :param result_code:期望返回
        :return:
        """
        testcase = xlrd.open_workbook(testcase_file)
        st = testcase.sheet_by_index(0)
        case_id = st.cell_value(caseId, 0)
        description = st.cell_value(caseId, 1)
        url = st.cell_value(caseId, 2)
        method = st.cell_value(caseId, 3)
        req_data = st.cell_value(caseId, 4)
        result_code = st.cell_value(caseId, 5)
        check_parm = st.cell_value(caseId, 6)
        case = [case_id, description, url, method,
                req_data, result_code, check_parm]
        return case

    def set_testCase_Color(self,
                           res,
                           tesetcase_file: str,
                           caseId: int,
                           sheetname: str,
                           writeB):
        """
        通过测试结果反馈来设置tesecase的颜色
        ：param case_id: 用例名称
        :param stylePaseBackground: 测试通过后单元格样式
        :param styleFailBackground: 测试失败后单元格样式
        """
        stylePassBackground = xlwt.easyxf(
            'pattern: pattern solid, fore_color green')  # 绿色
        styleFailBackground = xlwt.easyxf(
            'pattern: pattern solid, fore_color red')  # 红色
        if res:
            writeB.write(caseId, 1, "idfa_接口测试", stylePassBackground)
        else:
            writeB.write(caseId, 1, "idfa_接口测试", styleFailBackground)

    def do_excel_exec(self, testcase_file: str, caseId: int):
        """
        通过excel触发方法
        不走添加任务队列
        :param testcase_file:
        :param caseId:
        :return: bool
        """
        # if caseId == 0:
        #     caseId += 1
        res_data = self.get_testCase_info(testcase_file, caseId)
        print(res_data)
        url = res_data[2]
        method = res_data[3]
        params = res_data[4]
        res_list = []
        if method == "post":
            data = json.loads(params)
            res = self.do_method_reflect(url, method, data)
            if res:
                print(self.get_ujson_info(res))
                res_list.append(res.status_code)
        elif method == "get":
            res = self.do_method_reflect(url, method, params)
            if res:
                res_list.append(res.status_code)
        else:
            res_list.append('没有执行')
        return res_list

    def get_ujson_info(self, res):
        return json.dumps(res.json(), ensure_ascii=False)
