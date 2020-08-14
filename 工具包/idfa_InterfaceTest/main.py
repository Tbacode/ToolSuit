# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-06-26 14:49:57
# @Last Modified by:   Tommy
# @Last Modified time: 2020-01-09 16:43:29
from interFaceTest import network
import ujson
from interFaceTest import config
import xlrd
from xlutils.copy import copy


class Main():
    """
    Main事务数量
    """

    __slots__ = ["results", "count"]

    def __init__(self):
        self.results = {}
        self.results["测试成功"] = 0
        self.results["测试失败"] = 0
        self.count = 1

    def client_init(self):
        """
        客户端init
        :return:
        """
        with open("interFaceTest/config.json") as fp:  # 读取配置
            config_data = fp.read()
        config_dict = ujson.loads(config_data)
        config.server_host = config_dict["server_host"]
        config.wait_time = config_dict["wait_time"]
        config.actioncount = config_dict["actioncount"]

    def run_main(self, keys: int, taskfd):
        res = network.manager.add_session(keys, taskfd)
        network.manager.set_new_headers(network.manager.HEADER)  # 设置新包头
        if res:
            self.results["测试成功"] += 1
            print("测试成功")
            print("-" * 20)
        else:
            self.results["测试失败"] += 1
            print("测试失败")
            print("-" * 20)
        self.count += 1


if __name__ == '__main__':
    m = Main()
    m.client_init()
    network.manager.get_file_rows()
    result = None
    testcase = xlrd.open_workbook(network.manager.casefile)
    writeS = copy(testcase)
    writeB = writeS.get_sheet(network.manager.sheetname)
    # 针对excel内的用例测试
    # for i in range(network.manager.casefile_rows):
    #     if i != 0:
    #         result = network.manager.do_excel_exec(network.manager.casefile, i)
    #         print(result)
    # time.sleep(10)
    # -----------------------------------------------------------
    # 针对与config内用例测试
    # for i in range(len(config.server_host)):
    #     m.run_main(i, network.manager.request_task(config.server_host[i]))
    #     time.sleep(config.wait_time)
    # print(network.manager.get_session_length())
    # print(m.results)
    # -----------------------------------------------------------
    # 针对excel用例成功统计
    for i in range(network.manager.casefile_rows):
        if i != 0:
            case_info = network.manager.get_testCase_info(
                network.manager.casefile, i)
            print("接口地址：{}".format(case_info[2]))
            request_task = network.manager.request_task(
                case_info[2], case_info[4], case_info[6], case_info[3])
            network.manager.set_testCase_Color(
                request_task, network.manager.casefile,
                i, network.manager.sheetname, writeB)
            m.run_main(i, request_task)
    writeS.save(network.manager.casefile)
    print(m.results)
