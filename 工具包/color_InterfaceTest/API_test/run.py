# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-27 15:20:23
# @Last Modified by:   Tommy
# @Last Modified time: 2020-05-29 18:58:56
import unittest
from BSTestRunner import BSTestRunner
from BSTestRunner import _TestResult
import time
from test_case.tool import Tool
import asyncio
import aiohttp
import json

test_dir = r"./test_case"
report_dir = r"./reports"
now = ""
# TC发布群
wechat_message_for_TC = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5aae35f3-110c-4729-b776-8ad6413127db"
wechat_upload_for_TC = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=5aae35f3-110c-4729-b776-8ad6413127db&type=file"

# QA内部模拟群
wechat_message_for_QA2 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0fe2abe3-08e7-4069-828d-fbeb22899a5e"
wechat_upload_for_QA2 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=0fe2abe3-08e7-4069-828d-fbeb22899a5e&type=file"

# QA群
wechat_message_for_QA = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8d4d7e76-547b-4a68-8dbb-1d9dad0ec8c1"
wechat_upload_for_QA = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=8d4d7e76-547b-4a68-8dbb-1d9dad0ec8c1&type=file"

# is_test_mode = True
is_test_mode = False


def add_testCase(test_dir):
    # 加载测试用例
    if is_test_mode:
        discover = unittest.defaultTestLoader.discover(
            test_dir, pattern='tapcolor_test.py')
    else:
        discover = unittest.defaultTestLoader.discover(
            test_dir, pattern='tapcolor_api_*.py')
        # discover = unittest.defaultTestLoader.discover(test_dir, pattern='tapcolor_test.py')
    return discover


# 定义报告的文件格式
def get_report_dir(report_dir):
    report_dir = report_dir + '/' + now + '_test_report.html'
    return report_dir


# 运行用例并生成测试报告
def run_testCase(report_name, discover):
    # BSTestRunner生成网页测试报表
    with open(report_name, 'wb') as report_file:
        runner = BSTestRunner(stream=report_file,
                              title="TapColor API Test Report",
                              description="TapColor API Test Report")
        test_result = runner.run(discover)
        print(test_result)
        return test_result

        # TextTestRunner生成文本测试报表
    # with open(report_name, 'a') as report_file:
    #    runner = unittest.TextTestRunner(stream=report_file, verbosity=2)
    #    return runner.run(discover)


async def send_request(url, report_dir):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file_1',
                       open(report_dir, 'rb'),
                       filename=now + 'testReport.html',
                       content_type='multipart/form-data')
        async with session.post(url, data=data) as resp:
            print(await resp.text())
            return await resp.text()


def make_report_data(test_result: _TestResult):
    report_data = ""

    report_data = report_data + "test result  run: "
    report_data = report_data + str(test_result.testsRun)
    report_data = report_data + "  fail: " + str(test_result.failure_count)
    report_data = report_data + "  error: " + str(test_result.error_count)

    if test_result.failure_count == 0 and test_result.error_count == 0:
        return report_data
    else:
        report_data = report_data + "\n"
        report_data = report_data + "see more detail:"
        return report_data


def sent_wechat(my_report, report_data, wechat_message_url, wechat_upload_url):
    Tool.call_wechat_txt(wechat_message_url, report_data)
    print("api_test:get media_id")
    mytext = asyncio.run(send_request(wechat_upload_url, my_report))
    data = json.loads(mytext)
    my_id = data['media_id']
    Tool.call_wechat_media(wechat_message_url, my_id)


if __name__ == '__main__':
    now = time.strftime("%Y_%m_%d_%H_%M")

    print("api_test:add_testCase")
    my_discover = add_testCase(test_dir)

    print("api_test:get_report_name")
    my_report = get_report_dir(report_dir)

    print("api_test:run_testCase")
    test_result = run_testCase(my_report, my_discover)
    report_data = make_report_data(test_result)

    if test_result.failure_count != 0:
        if is_test_mode:
            sent_wechat(my_report, report_data, wechat_message_for_QA2,
                        wechat_upload_for_QA2)
        else:
            sent_wechat(my_report, report_data, wechat_message_for_TC,
                        wechat_upload_for_TC)
    elif test_result.error_count != 0:
        sent_wechat(my_report, report_data, wechat_message_for_QA,
                    wechat_upload_for_QA)

    # if check_result(test_result) :

    # print(my_result.printErrors())
