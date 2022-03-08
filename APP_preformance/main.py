'''
 * @Descripttion :
 * @Author       : Tommy
 * @Date         : 2021-10-15 12:07:39
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-02 18:18:18
'''
from logging import log
from Util_csv import UsingMyCsv
from Util_db import UsingMysql
from Util_pyecharts import UsingMyecharts
import datetime
from loguru import logger

m_csv = UsingMyCsv(
    r"C:\Users\talefun\Documents\ToolSuit\APP_preformance\TC_FPS.csv")


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


# # cpu_list = test('CPU', m_csv.get_data())
# print("--"*100)
# fps_list = test('FPS', m_csv.get_data())
# # print(cpu_list)
# # logger.error("数组长度：" + str(len(cpu_list)))


# # insert_db('hc_cpu20211026', 'CPU', 'TIME', cpu_list)
# insert_db('tc_fps20220302', 'FPS', 'TIME', fps_list)
# print(fps_list)


mem1_x, mem1_y = get_db_data("tc_fps20220302", "FPS")
mem2_x, mem2_y = get_db_data("tcp_fps20220302", "FPS")
mem3_x, mem3_y = get_db_data("hc_fps20220302", "FPS")
# cpu_x, cpu_y = get_db_data("tc_mem20211026", "MEM")
# fps_x, fps_y = get_db_data("pbn_mem20211026", "MEM")
# mem_old_x, mem_old_y = get_db_data("hc_mem20211026", "MEM")
# mem_pro_x, mem_pro_y = get_db_data("tcl_mem20211026", "MEM")




usecharts = UsingMyecharts(
    r"C:\Users\talefun\Documents\ToolSuit\APP_preformance\FPS_test.html")
# usecharts.page_simple_layout(mem_old_x, mem_y,fps_x, fps_y, mem_old_x, mem_old_y)
usecharts.page_simple_layout(mem1_x, mem1_y, mem2_x, mem2_y, mem3_x, mem3_y)