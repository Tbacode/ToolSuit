'''
 * @Descripttion :
 * @Author       : Tommy
 * @Date         : 2021-10-15 12:07:39
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-11-03 17:21:50
'''
from logging import log
from Util_csv import UsingMyCsv
from Util_db import UsingMysql
from Util_pyecharts import UsingMyecharts
import datetime
from loguru import logger

m_csv = UsingMyCsv(
    r"C:\Users\talefun\Documents\ToolSuit\APP_preformance\20211026HC性能测试.csv")


def test(key, data):
    time_stamp = 0
    flag = True
    info_list = []
    for item in data:

        if item[1][:3] == key:
            if flag:
                time_stamp = int(int(item[3]) / 1000)
                dateArray = datetime.datetime.fromtimestamp(
                    int(time_stamp / 1000))
                otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
                logger.debug("时间戳：" + str(otherStyleTime))
                flag = False
                item.append(otherStyleTime)
                info_list.append(item)
                time_stamp = time_stamp + 1000
            elif int(int(item[3]) / 1000) > time_stamp:
                time_stamp = int(int(item[3]) / 1000)
                dateArray = datetime.datetime.fromtimestamp(
                    int(time_stamp / 1000))
                otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
                # logger.debug("时间戳："+ str(otherStyleTime))
                item.append(otherStyleTime)
                info_list.append(item)
                time_stamp = time_stamp + 1000
    return info_list


def insert_db(table_name, table_key1, table_key2, data):
    for item in data:
        with UsingMysql(log_time=True) as um:
            sql = "insert into {}({}, {}) values(%s, %s)".format(
                table_name, table_key1, table_key2)
            um.insert_one(sql, item[4], item[-1])


def get_db_data(db_table_name, y_key, x_key="TIME"):
    data_x = []
    data_y = []
    with UsingMysql(log_time=True) as um:
        sql = "select * from {}".format(db_table_name)
        data = um.fetch_all(sql)
        for data_item in data:
            data_x.append(str(data_item[x_key]))
            data_y.append(int(data_item[y_key]))
    return data_x, data_y


# cpu_list = test('CPU', m_csv.get_data())
# print("--"*100)
# fps_list = test('FPS', m_csv.get_data())
# # print(cpu_list)
# logger.error("数组长度：" + str(len(cpu_list)))


# insert_db('hc_cpu20211026', 'CPU', 'TIME', cpu_list)
# insert_db('hc_fps20211026', 'FPS', 'TIME', fps_list)
# print(fps_list)


mem_x, mem_y = get_db_data("hc_mem20211026", "MEM")
cpu_x, cpu_y = get_db_data("hc_cpu20211026", "CPU")
fps_x, fps_y = get_db_data("hc_fps20211026", "FPS")




usecharts = UsingMyecharts(
    r"C:\Users\talefun\Documents\ToolSuit\APP_preformance\table1.html")
usecharts.set_table_echarts(mem_x, mem_y, cpu_x, cpu_y, fps_x, fps_y, "第一个")
