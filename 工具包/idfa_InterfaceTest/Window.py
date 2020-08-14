'''
@Descripttion: 窗口化idfa查询
@Author: Tommy
@Date: 2020-01-09 18:16:01
@LastEditors: Tommy
@LastEditTime: 2020-07-08 12:24:17
'''

import tkinter
import xlrd
import main
import json
from interFaceTest import network
from tkinter import ttk
from tkinter import scrolledtext
from xlutils.copy import copy


# 调用main的函数
def action_go():
    m = main.Main()
    m.client_init()
    network.manager.get_file_rows()
    # result = None
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
            network.manager.set_testCase_Color(request_task,
                                               network.manager.casefile, i,
                                               network.manager.sheetname,
                                               writeB)
            m.run_main(i, request_task)
    writeS.save(network.manager.casefile)
    print(m.results)
    result_scr.insert(tkinter.END, m.results)


# 数据构造函数
def get_idinfo_by_excel():
    testcase = xlrd.open_workbook("aa.xlsx")
    sheetname_list = testcase.sheet_names()
    if len(sheetname_list) > 1:
        print(sheetname_list[0])
        print(sheetname_list[1])
        sheetcase1 = testcase.sheet_by_name(sheetname_list[0])
        sheetcase2 = testcase.sheet_by_name(sheetname_list[1])
        # print(sheetcase1.nrows, sheetcase1.ncols)
        # print(sheetcase1.col_values(0))
        # print(type(sheetcase1.col_values(0, 2, 28)))
        return sheetcase1.col_values(0, 1,
                                     sheetcase1.nrows), sheetcase2.col_values(
                                         0, 1, sheetcase2.nrows)
    else:
        sheetcase1 = testcase.sheet_by_name(sheetname_list[0])
        return sheetcase1.col_values(0, 1, sheetcase1.nrows), None


# 构造测试用例
def set_case_in_excel(parm, testinfo, row):
    case = xlrd.open_workbook(network.manager.casefile)
    WriteObject = copy(case)
    Write = WriteObject.get_sheet("测试用例")
    Write.write(row, 0, row)
    Write.write(row, 1, "idfa_接口测试")
    Write.write(row, 2, "http://ad.weplayer.cc/adInfo")
    Write.write(row, 3, "post")
    Write.write(row, 4, parm)
    Write.write(row, 5, 200)
    Write.write(row, 6, str(testinfo))
    WriteObject.save(network.manager.casefile)


# 构造配置参数json串
def set_parm_by_json(idfa):
    json_dict = {}
    json_dict["platform"] = Version_system.get()
    json_dict["packageName"] = Object_game.get() + State_choose.get()
    json_dict["versionCode"] = entry_version.get()
    json_dict["idfa"] = idfa
    return json.dumps(json_dict)


def test():
    testinfo1, testinfo2 = get_idinfo_by_excel()
    print(testinfo1)
    for idfa_num in range(1, int(group_input_num.get()) + 2):
        parm = set_parm_by_json(idfa_num)
        print(parm)
        set_case_in_excel(parm, testinfo1, idfa_num)
    if testinfo2:
        for idfa_num in range(
                int(group_input_num.get()) + 2,
                2 * int(group_input_num.get()) + 3):
            parm = set_parm_by_json(idfa_num - int(group_input_num.get()) - 1)
            print(parm)
            set_case_in_excel(parm, testinfo2, idfa_num)
    action_go()


# 创建主窗口
window = tkinter.Tk()

# 设置标题
window.title("配置查询")

# 设置窗口大小
window.geometry('400x330')

# 创建各组件文字标题
version_title = tkinter.Label(window, text='请选择系统', font=("宋体", 10, "normal"))
version_title['fg'] = 'black'
version_title.place(x=0, y=80, width=150, height=20)

game_title = tkinter.Label(window, text='请选择游戏', font=("宋体", 10, "normal"))
game_title['fg'] = 'black'
game_title.place(x=120, y=20, width=150, height=20)

versionnum_title = tkinter.Label(window,
                                 text='请输入版本号',
                                 font=("宋体", 10, "normal"))
versionnum_title['fg'] = 'black'
versionnum_title.place(x=230, y=130, width=150, height=20)

State = tkinter.Label(window, text='请选择地区后缀', font=("宋体", 10, "normal"))
State['fg'] = 'black'
State.place(x=230, y=80, width=150, height=20)

group_num = tkinter.Label(window, text='请输入分组数', font=("宋体", 10, "normal"))
group_num['fg'] = 'black'
group_num.place(x=0, y=130, width=150, height=20)

# 创建分组数输入框
group_input = tkinter.Variable()
group_input_num = tkinter.Entry(window, textvariable=group_input)
group_input_num.place(x=20, y=150, width=150, height=20)

# 创建地区选择下拉框
State_title = tkinter.StringVar()
State_choose = ttk.Combobox(window, width=12, textvariable=State_title)
State_choose['values'] = ('', '-US', '-CA', '-AU', '-FR', '-GB', '-DE', '-MX',
                          '-IT', '-ES', '-CL', '-TH', '-CO', '-RU', '-GE',
                          '-BR', '-PT', '-BE', '-SE', '-CZ', '-JP', '-AT',
                          '-CH', '-PH', '-IN', '-AR')
State_choose['state'] = 'readonly'
State_choose.place(x=230, y=100, width=150, height=20)

# 创建系统选择下拉框
Version_sys = tkinter.StringVar()
Version_system = ttk.Combobox(window, width=12, textvariable=Version_sys)
Version_system['values'] = ('android', 'ios')
Version_system['state'] = 'readonly'
Version_system.place(x=20, y=100, width=150, height=20)
Version_system.current(0)

# 创建游戏选择下拉框
Object = tkinter.StringVar()
Object_game = ttk.Combobox(window, width=12, textvariable=Object)
Object_game['values'] = (
    'com.pixel.art.coloring.by.number',
    'com.relax.coloring.games.color.by.number.colourpop',
    'com.acoin.ballz.bricks.breaker', 'com.ball.brick.break',
    'coloring.color.number.happy.paint.art.drawing.puzzle')
Object_game['state'] = 'readonly'
Object_game.place(x=20, y=40, width=360, height=25)
Object_game.current(0)

# 创建输入文本框1--版本号输入
var_version = tkinter.Variable()
entry_version = tkinter.Entry(window, textvariable=var_version)
entry_version.place(x=230, y=150, width=150, height=20)

# 创建一个开始按钮
button = tkinter.Button(window,
                        text='开始',
                        bg='orange',
                        width=100,
                        height=50,
                        activebackground='orange',
                        activeforeground='white',
                        command=test)
button.place(x=150, y=185, width=100, height=50)

# 创建一个滚动文本框
result_scr = scrolledtext.ScrolledText(window,
                                       width=50,
                                       height=1,
                                       wrap=tkinter.WORD)
result_scr.place(x=20, y=255)

# 进入消息循环
window.mainloop()
