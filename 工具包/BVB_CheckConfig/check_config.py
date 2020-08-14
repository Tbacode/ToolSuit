'''
@Descripttion: 弹球关卡config检查脚本
@Author: Tommy
@Date: 2020-07-06 19:22:35
@LastEditors: Tommy
@LastEditTime: 2020-07-29 23:23:11
'''
import os
import json
import tkinter
from tkinter import scrolledtext
from tkinter import END
from tkinter import filedialog
from tkinter import ttk

start_Y, end_Y = 0, 0
noDown_block = []
noLife_block = []


def init(filename: str, index: int, res: dict, mode: bool) -> int:
    '''
    @name: init
    @msg: 每个关卡文件读取时，做公共数据的初始化
    @param {文件名}
    @return: int, int
    '''
    path = path_file.get() + "/" + filename
    with open(path, 'rb') as f:
        result = json.load(f)
    '''
    保险方式应该所有Y坐标去重，排序，取首位
    '''
    Y_list = []
    if mode is True:
        for item in range(1, len(result['data'][7])):
            Y_list.append(result['data'][7][item][1])
    else:
        if index <= 500:
            for item in range(1, len(result['data'][7])):
                Y_list.append(result['data'][7][item][1])
        else:
            for item in range(1, len(result['data'][7])):
                Y_list.append(result['data'][7][item][9])
    Y_list = list(set(sorted(Y_list)))
    global noDown_block, noLife_block
    noDown_block = res["noDownBlock"]
    noLife_block = res["noLifeBlock"]
    start_Y = Y_list[1]
    end_Y = Y_list[-1]
    json_data = result['data']
    return start_Y, end_Y, json_data


def get_filesname_by_suffixes(path: str,
                              suffixe: str = 'json',
                              traverse: bool = False) -> list:
    '''
    @name: get_filesname_by_suffixes
    @msg: 返回指定后缀的文件名
    @param {路径, 后缀, bool}
    @return: list
    '''
    name_list = []
    for root, dirs, files in os.walk(path):
        if not traverse:
            for file in files:
                file_suffix = os.path.splitext(file)[1][1:].lower()
                if file_suffix in suffixe:
                    # name_list.append(os.path.splitext(file)[0][:])
                    name_list.append(file)
    return name_list


def isDropblock(data: list, index: int, item: str, mode: bool):
    '''
    @name: isDropblock
    @msg: 检查关卡配置是否存在无法下落砖块存在战斗界面之上
    @param {砖块坐标数据, 标记变量, 文件名}
    @return: none
    '''
    if mode is True:
        for i in range(1, len(data)):
            if data[i][1] > 12:
                if data[i][2] in noDown_block:
                    # print("存在不可下落砖块在战斗界面之上: {}".format(data[i]))
                    result_scr2.insert(
                        tkinter.END,
                        "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                    result_scr2.insert(
                        tkinter.END,
                        "存在不可下落砖块在战斗界面之上: {}".format(data[i]) + "\n")
                    result_scr2.see(END)
                    result_scr2.update()
    else:
        if index <= 500:
            for i in range(1, len(data)):
                if data[i][1] > 12:
                    if data[i][2] in noDown_block:
                        # print("存在不可下落砖块在战斗界面之上: {}".format(data[i]))
                        result_scr2.insert(
                            tkinter.END,
                            "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                        result_scr2.insert(
                            tkinter.END,
                            "存在不可下落砖块在战斗界面之上: {}".format(data[i]) + "\n")
                        result_scr2.see(END)
                        result_scr2.update()
        else:
            for i in range(1, len(data)):
                if data[i][9] > 12:
                    if data[i][10] in noDown_block:
                        # print("存在不可下落砖块在战斗界面之上: {}".format(data[i]))
                        result_scr2.insert(
                            tkinter.END,
                            "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                        result_scr2.insert(
                            tkinter.END,
                            "存在不可下落砖块在战斗界面之上: {}".format(data[i]) + "\n")
                        result_scr2.see(END)
                        result_scr2.update()


def isEmpty(end_Y: int, data: list, index: int, item: str, mode: bool):
    '''
    @name: isEmpty
    @msg: 检查关卡配置是否存在空行存在战斗界面之上
    @param {结束Y坐标, 砖块坐标数据, 标记变量, 文件名}
    @return: none
    '''
    contrast_list = [i for i in range(13, end_Y + 1)]
    default_list = []
    if mode is True:
        for i in range(1, len(data)):
            if data[i][1] > 12:
                default_list.append(data[i][1])
    else:
        if index <= 500:
            for i in range(1, len(data)):
                if data[i][1] > 12:
                    default_list.append(data[i][1])
        else:
            for i in range(1, len(data)):
                if data[i][9] > 12:
                    default_list.append(data[i][9])
    default_list = list(set(default_list))
    difference_list = [
        dir_item for dir_item in contrast_list if dir_item not in default_list
    ]
    if len(difference_list):
        result_scr2.insert(tkinter.END,
                           "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
        result_scr2.insert(tkinter.END,
                           "存在空行异常 Y={}".format(difference_list) + "\n")
        result_scr2.see(END)
        result_scr2.update()
        # print("存在空行异常 Y={}".format(difference_list))


def isXerror(data: list, index: int, item: str, mode: bool):
    '''
    @name: isXerror
    @msg: 检查X坐标是否超出上限
    @param {砖块坐标数据, 标记变量, 文件名}
    @return: none
    '''
    if mode is True:
        for i in range(1, len(data)):
            if data[i][0] > 10:
                result_scr2.insert(
                    tkinter.END,
                    "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                result_scr2.insert(tkinter.END,
                                   "X坐标存在大于10的异常: {}".format(data[i]) + "\n")
                result_scr2.see(END)
                result_scr2.update()
    else:
        if index <= 500:
            for i in range(1, len(data)):
                if data[i][0] > 10:
                    result_scr2.insert(
                        tkinter.END,
                        "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                    result_scr2.insert(
                        tkinter.END, "X坐标存在大于10的异常: {}".format(data[i]) + "\n")
                    result_scr2.see(END)
                    result_scr2.update()
                    # print("X坐标存在大于10的异常: {}".format(data[i]))
        else:
            for i in range(1, len(data)):
                if data[i][8] > 10:
                    result_scr2.insert(
                        tkinter.END,
                        "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                    result_scr2.insert(
                        tkinter.END, "X坐标存在大于10的异常: {}".format(data[i]) + "\n")
                    result_scr2.see(END)
                    result_scr2.update()
                    # print("X坐标存在大于10的异常: {}".format(data[i]))


def isBlockLifeEmpty(data: list, index: int, item: str, mode: bool):
    '''
    @name: isBlockLifeEmpty
    @msg: 检查砖块血量是否为0的异常
    @param {砖块坐标数据, 标记变量, 文件名}
    @return: none
    '''
    if mode is True:
        for i in range(1, len(data)):
            if data[i][2] not in noLife_block:
                if data[i][3]["num"] <= 0:
                    result_scr2.insert(
                        tkinter.END,
                        "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                    result_scr2.insert(tkinter.END,
                                       "存在砖块生命为0：{}".format(data[i]) + "\n")
                    result_scr2.see(END)
                    result_scr2.update()
                    # print("存在砖块生命为0：{}".format(data[i]))
    else:
        if index <= 500:
            for i in range(1, len(data)):
                if data[i][2] not in noLife_block:
                    if data[i][3]["num"] <= 0:
                        result_scr2.insert(
                            tkinter.END,
                            "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                        result_scr2.insert(
                            tkinter.END, "存在砖块生命为0：{}".format(data[i]) + "\n")
                        result_scr2.see(END)
                        result_scr2.update()
                        # print("存在砖块生命为0：{}".format(data[i]))
        else:
            for i in range(1, len(data)):
                if data[i][10] not in noLife_block:
                    if data[i][7] <= 0:
                        result_scr2.insert(
                            tkinter.END,
                            "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                        result_scr2.insert(
                            tkinter.END, "存在砖块生命为0：{}".format(data[i]) + "\n")
                        result_scr2.see(END)
                        result_scr2.update()
                        # print("存在砖块生命为0：{}".format(data[i]))


def isHideBlockError(data: list, index: int, item: str, mode: bool):
    '''
    @name: isHideBlockError
    @msg: 检查隐藏砖块是否Y坐标大于12
    @param {砖块坐标数据, 标记变量, 文件名}
    @return: none
    '''
    if mode is True:
        for i in range(1, len(data)):
            if data[i][2] == 38:
                if data[i][1] > 12:
                    result_scr2.insert(
                        tkinter.END,
                        "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                    result_scr2.insert(
                        tkinter.END,
                        "存在隐藏砖块Y坐标大于12: {}".format(data[i]) + "\n")
                    result_scr2.see(END)
                    result_scr2.update()
                    # print("存在隐藏砖块Y坐标大于12: {}".format(data[i]))
    else:
        if index <= 500:
            for i in range(1, len(data)):
                if data[i][2] == 38:
                    if data[i][1] > 12:
                        result_scr2.insert(
                            tkinter.END,
                            "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                        result_scr2.insert(
                            tkinter.END,
                            "存在隐藏砖块Y坐标大于12: {}".format(data[i]) + "\n")
                        result_scr2.see(END)
                        result_scr2.update()
                        # print("存在隐藏砖块Y坐标大于12: {}".format(data[i]))
        else:
            for i in range(1, len(data)):
                if data[i][10] == 38:
                    if data[i][9] > 12:
                        result_scr2.insert(
                            tkinter.END,
                            "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
                        result_scr2.insert(
                            tkinter.END,
                            "存在隐藏砖块Y坐标大于12: {}".format(data[i]) + "\n")
                        result_scr2.see(END)
                        result_scr2.update()
                        # print("存在隐藏砖块Y坐标大于12: {}".format(data[i]))


def isPortalBlockDoubleExist(data: list, index: int, item: str, mode: bool):
    '''
    @name: isPortalBlockDoubleExist
    @msg: 检查传送门砖块是否成对出现
    @param {砖块坐标数据, 标记变量, 文件名}
    @return: none
    '''
    flag = 0
    Portal_list = []
    if mode is True:
        for i in range(1, len(data)):
            if data[i][2] == 24:
                flag += 1
                Portal_list.append(data[i])
    else:
        if index <= 500:
            for i in range(1, len(data)):
                if data[i][2] == 24:
                    flag += 1
                    Portal_list.append(data[i])
        else:
            for i in range(1, len(data)):
                if data[i][10] == 24:
                    flag += 1
                    Portal_list.append(data[i])
    if flag % 2 != 0:
        result_scr2.insert(tkinter.END,
                           "*" * 10 + "关卡：{}".format(item) + "*" * 10 + "\n")
        result_scr2.insert(tkinter.END,
                           "存在传送门砖块不成对的异常: {}".format(Portal_list) + "\n")
        result_scr2.see(END)
        result_scr2.update()
        # print("存在传送门砖块不成对的异常: {}".format(Portal_list))


def main():
    result_scr2.delete(1.0, tkinter.END)
    result_scr1.delete(1.0, tkinter.END)
    with open("config.json", "rb") as f:
        res = json.load(f)
    if path_file.get() == "":
        result_scr2.insert(tkinter.END, "请选择关卡文件夹" + "\n")
        result_scr2.see(END)
        result_scr2.update()
    else:
        name = get_filesname_by_suffixes(path_file.get())
    if mode_type_box.get() == "全新":
        mode = True
    else:
        mode = False
    for item in name:
        index = int(item.split(".")[0].split("_")[1])
        # print("*" * 10 + "正在检查关卡：{}".format(item) + "*" * 10)
        result_scr1.insert(
            tkinter.END, "*" * 10 + "正在检查关卡：{}".format(item) + "*" * 10 + "\n")
        result_scr1.see(END)
        result_scr1.update()
        x, y, json_data = init(item, index, res, mode)
        isDropblock(json_data[7], index, item, mode)
        isEmpty(y, json_data[7], index, item, mode)
        isXerror(json_data[7], index, item, mode)
        isBlockLifeEmpty(json_data[7], index, item, mode)
        isHideBlockError(json_data[7], index, item, mode)
        isPortalBlockDoubleExist(json_data[7], index, item, mode)
    result_scr1.insert(tkinter.END, "*" * 10 + "检查结束" + "*" * 10)


def change_nolife_config():
    nolifeType_num = nolife_type.get()
    if nolifeType_num != "":
        with open("config.json", "rb") as f:
            res = json.load(f)
        res["noLifeBlock"].append(int(nolifeType_num))
        res["noLifeBlock"] = list(set(res["noLifeBlock"]))
        with open("config.json", "w+", encoding='utf-8') as a:
            json.dump(res, a, ensure_ascii=False)
    else:
        result_scr2.insert(tkinter.END, "增加无生命砖块为空" + "\n")
        result_scr2.see(END)
        result_scr2.update()


def change_nodown_config():
    nodownType_num = nodown_type.get()
    if nodownType_num != "":
        with open("config.json", "rb") as f:
            res = json.load(f)
        res["noDownBlock"].append(int(nodownType_num))
        res["noDownBlock"] = list(set(res["noDownBlock"]))
        with open("config.json", "w+", encoding='utf-8') as a:
            json.dump(res, a, ensure_ascii=False)
    else:
        result_scr2.insert(tkinter.END, "增加无下落砖块为空" + "\n")
        result_scr2.see(END)
        result_scr2.update()


def find_filePath():
    path_file.delete(0, tkinter.END)
    filePath = filedialog.askdirectory()
    path_file.insert(tkinter.END, filePath)


# 创建主窗口
window = tkinter.Tk()

# 设置标题
window.title("配置查询")

# 设置窗口大小
window.geometry('610x700')

# 创建各组件文字标题
result_scr1_title0 = tkinter.Label(window,
                                   text='模式：',
                                   font=("宋体", 10, "normal"))
result_scr1_title0['fg'] = 'black'
result_scr1_title0.place(x=0, y=20, width=85, height=25)

# 创建模式选择下拉框
tpye_box = tkinter.StringVar()
mode_type_box = ttk.Combobox(window, width=12, textvariable=tpye_box)
mode_type_box['values'] = ('全新', '前500新')
mode_type_box.place(x=60, y=20, width=80, height=25)
mode_type_box.current(0)
mode_type_box['state'] = 'readonly'

# 创建一个开始按钮
button = tkinter.Button(window,
                        text='开始',
                        bg='orange',
                        activebackground='orange',
                        activeforeground='white',
                        command=main)
button.place(x=150, y=20, width=440, height=25)

# 创建各组件文字标题
result_scr1_title1 = tkinter.Label(window,
                                   text='输出日志',
                                   font=("宋体", 10, "normal"))
result_scr1_title1['fg'] = 'black'
result_scr1_title1.place(x=0, y=65, width=100, height=20)

# 创建各组件文字标题
result_scr1_title2 = tkinter.Label(window,
                                   text='警告日志',
                                   font=("宋体", 10, "normal"))
result_scr1_title2['fg'] = 'black'
result_scr1_title2.place(x=0, y=290, width=100, height=20)

# 创建一个滚动文本框
result_scr1 = scrolledtext.ScrolledText(window,
                                        width=80,
                                        height=15,
                                        wrap=tkinter.WORD)
result_scr1.place(x=20, y=85)

# 创建一个滚动文本框
result_scr2 = scrolledtext.ScrolledText(window,
                                        width=80,
                                        height=20,
                                        wrap=tkinter.WORD)
result_scr2.place(x=20, y=310)

# 创建增加无生命砖块输入框
nolife_txt = tkinter.Variable()
nolife_type = tkinter.Entry(window, textvariable=nolife_txt)
nolife_type.place(x=20, y=585, width=250, height=25)

# 创建一个增加无生命砖块按钮
button = tkinter.Button(window,
                        text='增加无生命砖块属性值',
                        bg='orange',
                        activebackground='orange',
                        activeforeground='white',
                        command=change_nolife_config)
button.place(x=340, y=585, width=250, height=25)

# 创建增加无法下落砖块输入框
nodown_txt = tkinter.Variable()
nodown_type = tkinter.Entry(window, textvariable=nodown_txt)
nodown_type.place(x=20, y=620, width=250, height=25)

# 创建一个增加无法下落砖块按钮
button = tkinter.Button(window,
                        text='增加无下落砖块属性值',
                        bg='orange',
                        activebackground='orange',
                        activeforeground='white',
                        command=change_nodown_config)
button.place(x=340, y=620, width=250, height=25)

# 创建文件路径输入框
path_txt = tkinter.Variable()
path_file = tkinter.Entry(window, textvariable=path_txt)
path_file.place(x=20, y=655, width=450, height=25)

# 创建一个寻找路径按钮
button = tkinter.Button(window,
                        text='文件夹选择',
                        bg='orange',
                        activebackground='orange',
                        activeforeground='white',
                        command=find_filePath)
button.place(x=500, y=655, width=90, height=25)

# 进入消息循环
window.mainloop()
