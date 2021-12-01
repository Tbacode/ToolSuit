# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-17 17:10:04
# @Last Modified by:   Tommy
# @Last Modified time: 2019-10-16 17:29:31
import subprocess
import time
import os
# from pyecharts import Line, Grid
from pyecharts.charts import Grid, Line
from pyecharts import options as opts
from selenium import webdriver
from Util_db import UsingMysql

time_value = []
JavaHeap_value = []
NativeHeap_value = []
Code_value = []
Stack_value = []
Graphics_value = []
PrivateOther_value = []
System_value = []
TOTAL_PSS_value = []
TOTAL_RSS_value = []


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


# 内存占用情况 com.pixel.art.coloring.by.number com.brick.breaker.ball.shooting.blast
# tcl com.pixel.art.coloring.by.number
def get_mem_using(package_name="com.pixel.art.coloring.by.number"):
    """查看apk的内存占用
    :param package_name:
    :return: 单位KB
    """
    if not package_name:
        package_name = get_apk_info()[0]
    results = run_cmd("adb shell dumpsys meminfo {}".format(package_name))
    for index, result in enumerate(results):
        if result.strip().startswith('TOTAL PSS'):
            return results[index]


# 对cmd格式进行重组，返回成dict
def main():
    dicts = {}
    result = get_mem_using()
    # for i in result[:len(result) - 2]:
    #     if i.strip():
    #         dicts[i.split(':')[0].strip()] = i.split(':')[1].strip().split(' ')[0].strip()
    # p = result[-1].split('TOTAL')
    p = result.split('TOTAL')
    dicts[('TOTAL' + p[1]).split(':')[0]
          ] = ('TOTAL' + p[1]).split(':')[1].strip()
    # dicts[('TOTAL' + p[2]).split(':')[0]
    #       ] = ('TOTAL' + p[2]).split(':')[-1].strip()
    return dicts


# pyecharts方法
def pyecharts_set(dicts, i):
    time_value.append(str(i * 5))
    # 获得的数据均为KB在图表中不能显示微小变化，以四舍五入方式转为MB
    # JavaHeap_value.append(round(int(dicts['Java Heap']) / 1024))
    # NativeHeap_value.append(round(int(dicts['Native Heap']) / 1024))
    # Code_value.append(round(int(dicts['Code']) / 1024))
    # Stack_value.append(round(int(dicts['Stack']) / 1024))
    # Graphics_value.append(round(int(dicts['Graphics']) / 1024))
    # PrivateOther_value.append(round(int(dicts['Private Other']) / 1024))
    # System_value.append(round(int(dicts['System']) / 1024))
    TOTAL_PSS_value.append(round(int(dicts['TOTAL PSS']) / 1024))
    # TOTAL_RSS_value.append(round(int(dicts['TOTAL RSS']) / 1024))
    # line = Line('APP_Summary HTML BBB 4.0.0')
    # line.add('Java Heap', time_value, JavaHeap_value, is_smooth=True)
    # line.add('Native Heap', time_value, NativeHeap_value, is_smooth=True)
    # line.add('Code', time_value, Code_value, is_smooth=True)
    # line.add('Stack', time_value, Stack_value, is_smooth=True)
    # line.add('Graphics', time_value, Graphics_value, is_smooth=True)
    # line.add('Private Other', time_value,
    #          PrivateOther_value, is_smooth=True)
    # line.add('System', time_value, System_value, s_smooth=True)
    # line.add('TOTAL', time_value, TOTAL_PSS_value,
    #          is_smooth=True, mark_point=['average', 'max'])
    # line.add('TOTAL SWAP PSS', time_value,
    #          TOTAL_RSS_value, is_smooth=True)
    line = (
        Line()
        .add_xaxis(time_value)
        .add_yaxis("内存", y_axis=TOTAL_PSS_value, symbol="emptyCircle", is_smooth=True, label_opts=opts.LabelOpts(is_show=False), markpoint_opts=opts.MarkLineOpts(data=[opts.MarkPointItem(name='平均值', type_='average'), opts.MarkPointItem(name='峰值', type_='max')]))
        .set_global_opts(title_opts=opts.TitleOpts(title="折线图-基本示例"),
                         datazoom_opts=opts.DataZoomOpts())
    )
    # grid = (
    #     Grid()
    #     .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
    # )

    line.render(
        r'C:\Users\talefun\Documents\ToolSuit\工具包\APP_Summary\APP_Summary.html')


if __name__ == '__main__':
    i = 1
    # driver = webdriver.Chrome()
    # options = webdriver.ChromeOptions()

    # 忽略无用的日志
    # options.add_experimental_option(
    #     "excludeSwitches", ['enable-automation', 'enable-logging'])
    # driver = webdriver.Chrome(chrome_options=options)
    # driver.get(r'https://192.168.1.1')

    

    while True:
        with UsingMysql(log_time=True) as um:
            sql = "insert into tcl_mem20211110(MEM, TIME) values(%s, %s)"
            print("写入第 {} 次数据！".format(i))
            dicts = main()
            um.insert_one(sql, int(dicts['TOTAL PSS']) / 1024, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # if i == 1:
        #     # init_to_excel(dicts)
        #     pyecharts_set(dicts, i)
        #     driver.get(
        #         r'C:\Users\talefun\Documents\ToolSuit\工具包\APP_Summary\APP_Summary.html')  # 这里需要填写绝对路径，相对路径是相对与chromedriver的
        # else:
        #     # add_to_excel(dicts, i)
        #     pyecharts_set(dicts, i)
        #     driver.refresh()  # 刷新html
        time.sleep(1)
        i += 1
