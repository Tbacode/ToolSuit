'''
Descripttion: 111
Author: Tommy
Date: 2019-05-27 15:20:23
LastEditors: Tommy
LastEditTime: 2020-08-11 11:10:36
'''
# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-27 15:20:23
# @Last Modified by:   Tommy
# @Last Modified time: 2020-05-29 18:58:56
import unittest
from BSTestRunner import BSTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import os
import time


user = '875932826'
pwd = 'tjztoslvzbstbbbc'
sender = '875932826@qq.com'
receiver_list = ['xt875932826@126.com']


def send_mail(file_new, receiver_list):
    '''定义发送邮件'''
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    sendfile = open(file_new, 'rb').read()

    att = MIMEText(sendfile, 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="report.html"'

    msgRoot = MIMEMultipart()
    msgRoot.attach(MIMEText(mail_body, 'html', 'utf-8'))
    msgRoot['Subject'] = Header("自动化测试报告", 'utf-8')
    msgRoot.attach(att)

    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
    smtp.login(user, pwd)
    for x in receiver_list:
        smtp.sendmail(sender,
                      x,
                      msgRoot.as_string())
    print('email has send out')


def new_report(testreport):
    '''查找时间最接近的report'''
    lists = os.listdir(testreport)
    lists.sort(key=lambda fn: os.path.getmtime(testreport + "\\" + fn))
    file_new = os.path.join(testreport, lists[-1])
    print(file_new)
    return file_new


# 指定测试用例和测试报告的路径
test_dir = r"./test_case"
report_dir = r"./reports"

# 加载测试用例
discover = unittest.defaultTestLoader.discover(
    test_dir, pattern='tapcolor_*.py')

# 定义报告的文件格式
now = time.strftime("%Y-%m-%d %H_%M_%S")
report_name = report_dir + '/' + now + ' test_report.html'

# 运行用例并生成测试报告
with open(report_name, 'wb') as f:
    runner = BSTestRunner(stream=f, title="TapColor API Test Report",
                          description="TapColor API Test Report")
    runner.run(discover)

new_report = new_report(report_dir)
send_mail(new_report, receiver_list)
