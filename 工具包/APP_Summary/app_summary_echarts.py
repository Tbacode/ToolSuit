# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-17 17:10:04
# @Last Modified by:   Tommy
# @Last Modified time: 2019-10-16 17:29:31
import subprocess
import time
import os
from pyecharts import Line
from selenium import webdriver

time_value = []
JavaHeap_value = []
NativeHeap_value = []
Code_value = []
Stack_value = []
Graphics_value = []
PrivateOther_value = []
System_value = []
TOTAL_value = []
TOTAL_SWAP_PSS_value = []


# cmd命令执行代码
def run_cmd(cmd):
    """执行CMD命令"""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return [i.decode() for i in p.communicate()[0].splitlines()]


# 获取APK的名称
def get_apk_info():
    """获取apk的package，activity名称
        :return: list  eg ['com.android.calendar',
        'com.meizu.flyme.calendar.AllInOneActivity']
    """
    result = os.popen(
        'adb shell dumpsys activity top | find "ACTIVITY"').read()
    return result.splitlines()[-1].split()[1].split('/')


# 内存占用情况
def get_mem_using(package_name=None):
    """查看apk的内存占用
    :param package_name:
    :return: 单位KB
    """
    if not package_name:
        package_name = get_apk_info()[0]
    results = run_cmd("adb shell dumpsys meminfo {}".format(package_name))
    for index, result in enumerate(results):
        if result.strip().startswith('Java Heap'):
            return results[index:index + 10]


# 对cmd格式进行重组，返回成dict
def main():
    dicts = {}
    result = get_mem_using()
    for i in result[:len(result) - 2]:
        if i.strip():
            dicts[i.split(':')[0].strip()] = i.split(':')[1].strip()
    p = result[-1].split('TOTAL')
    dicts[('TOTAL' + p[1]).split(':')[0]
          ] = ('TOTAL' + p[1]).split(':')[1].strip()
    dicts[('TOTAL' + p[2]).split(':')[0]
          ] = ('TOTAL' + p[2]).split(':')[-1].strip()
    return dicts


# pyecharts方法
def pyecharts_set(dicts, i):
    time_value.append(i * 5)
    # 获得的数据均为KB在图表中不能显示微小变化，以四舍五入方式转为MB
    JavaHeap_value.append(round(int(dicts['Java Heap']) / 1024))
    NativeHeap_value.append(round(int(dicts['Native Heap']) / 1024))
    Code_value.append(round(int(dicts['Code']) / 1024))
    Stack_value.append(round(int(dicts['Stack']) / 1024))
    Graphics_value.append(round(int(dicts['Graphics']) / 1024))
    PrivateOther_value.append(round(int(dicts['Private Other']) / 1024))
    System_value.append(round(int(dicts['System']) / 1024))
    TOTAL_value.append(round(int(dicts['TOTAL']) / 1024))
    TOTAL_SWAP_PSS_value.append(round(int(dicts['TOTAL SWAP PSS']) / 1024))
    line = Line('APP_Summary HTML')
    line.add('Java Heap', time_value, JavaHeap_value, is_smooth=True)
    line.add('Native Heap', time_value, NativeHeap_value, is_smooth=True)
    line.add('Code', time_value, Code_value, is_smooth=True)
    line.add('Stack', time_value, Stack_value, is_smooth=True)
    line.add('Graphics', time_value, Graphics_value, is_smooth=True)
    line.add('Private Other', time_value,
             PrivateOther_value, is_smooth=True)
    line.add('System', time_value, System_value, s_smooth=True)
    line.add('TOTAL', time_value, TOTAL_value,
             is_smooth=True, mark_point=['average', 'max'])
    line.add('TOTAL SWAP PSS', time_value,
             TOTAL_SWAP_PSS_value, is_smooth=True)
    line.render('APP_Summary.html')


if __name__ == '__main__':
    i = 1
    driver = webdriver.Chrome()
    while True:
        print("写入第 {} 次数据！".format(i))
        dicts = main()
        if i == 1:
            # init_to_excel(dicts)
            pyecharts_set(dicts, i)
            driver.get(
                r'C:\Users\xt875\Desktop\脚本\APP_Summary\APP_Summary.html')  # 这里需要填写绝对路径，相对路径是相对与chromedriver的
        else:
            # add_to_excel(dicts, i)
            pyecharts_set(dicts, i)
            driver.refresh()  # 刷新html
        time.sleep(1)
        i += 1
