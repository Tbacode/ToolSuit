'''
@Descripttion: 配置查询窗口化
@Author: Tommy
@Date: 2019-04-28 11:41:32
@LastEditors: Tommy
@LastEditTime: 2020-07-08 16:00:17
'''

import tkinter
import json
import requests
from tkinter import ttk
from tkinter import scrolledtext


# 请求
def apireturn(platform, packname, visioncode, state, idfa):
    url = 'http://ad.weplayer.cc/adInfo'
    data = {
        "platform": platform,
        "packageName": packname + state,
        "versionCode": visioncode,
        "idfa": idfa
    }
    print(data)
    headers = {"Content-Type": "application/json", "Accept": "text/plain"}
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.url)
    res_init = json.dumps(res.json(),
                          indent=2,
                          sort_keys=True,
                          ensure_ascii=False)  # res.json()
    res_dict = json.loads(res_init)

    return res_dict


# 这里作初始化的变量赋值，为后续请求作参数数据
def init_data():
    version_system = Version_system.get()
    game_name = Object_game.get()
    version_num = entry_version.get()
    state_des = State_choose.get()
    idfa = idfa_input_num.get()
    return version_system, game_name, version_num, state_des, idfa


# action_go按钮方法
def action_go():
    version_system, game_name, version_num, state_des, idfa = init_data()
    if version_num == '':  # 容错处理
        result_scr.insert(tkinter.END, "版本号不能为空！！！！")
    else:
        print(version_system, game_name, version_num, state_des)
        result_scr.delete(1.0, tkinter.END)  # 删除默认值后，重新赋值
        data_result = apireturn(version_system, game_name, version_num,
                                state_des, idfa)
        keyword_select1['values'] = list_key_select(data_result)
        keyword_select1.current(0)
        keyword_select2['values'] = list_key_select(
            data_result[keyword_select1.get()])
        keyword_select2.current(0)
        result = json.dumps(
            data_result[keyword_select1.get()][keyword_select2.get()],
            indent=1)
        result_scr.insert(tkinter.END, result)
        button_find['state'] = 'normal'


# 获取data参数的key值返回
def list_key_select(data):
    '''
    这里坐容错处理
    '''
    if type(data) == dict:  # 如果参数是个字典，返回list形式的key
        return list(dict(data).keys())
    elif data:  # 不是dict就是list，可直接返回下拉框，下拉框直接接受list形式数据
        return data
    else:
        return "无参数"


# 选择框1点击绑定事件
def value_list_get(*args):
    # 每次的点击事件后，都要重新请求否则数据为空
    version_system, game_name, version_num, state_des, idfa = init_data()
    data_result = apireturn(version_system, game_name, version_num, state_des,
                            idfa)
    keyword_select2['values'] = list_key_select(
        data_result[keyword_select1.get()])
    keyword_select2.current(0)
    if keyword_select2.get() != '无参数':
        result_scr.delete(1.0, tkinter.END)  # 删除默认值后，重新赋值
        result = json.dumps(
            data_result[keyword_select1.get()][keyword_select2.get()],
            indent=1)
        result_scr.insert(tkinter.END, result)
    else:
        result_scr.delete(1.0, tkinter.END)
        result_scr.insert(tkinter.END, "空值")


# 选择框2点击绑定事件
def value_result(*args):
    # 每次的点击事件后，都要重新请求否则数据为空
    version_system, game_name, version_num, state_des, idfa = init_data()
    data_result = apireturn(version_system, game_name, version_num, state_des,
                            idfa)
    if keyword_select2.get() != '无参数':
        result_scr.delete(1.0, tkinter.END)  # 删除默认值后，重新赋值
        result = json.dumps(
            data_result[keyword_select1.get()][keyword_select2.get()],
            indent=1)
        result_scr.insert(tkinter.END, result)
    else:
        result_scr.delete(1.0, tkinter.END)
        result_scr.insert(tkinter.END, "空值")


# 获取文本框中信息
def getinfo_By_textwin():
    result = result_scr.get("1.0", "end-1c")
    keyword_result = keyword.get()
    find_By_textwin(result, keyword_result)


# 查找匹配项
def find_By_textwin(result, keyword_result):
    result_list = []
    if keyword_result == "":
        keyword.insert(tkinter.END, "空值")
    else:
        keyword_list = keyword_result.split(",")
        if len(keyword_list) == 1:
            position = result.find(keyword_result[0])
            if position != -1:
                result_scr.delete(1.0, tkinter.END)
                result_scr.insert(tkinter.END, "匹配到 {}".format(keyword_result))
            else:
                result_scr.delete(1.0, tkinter.END)
                result_scr.insert(tkinter.END,
                                  "无法匹配 {}".format(keyword_result))

        elif len(keyword_list) > 1:
            for item in keyword_list:
                position = result.find(item)
                result_list.append(position)
            result_scr.delete(1.0, tkinter.END)
            for index, result_item in enumerate(result_list):
                if result_item == -1:
                    result_scr.insert(tkinter.END,
                                      "无法匹配 {}".format(keyword_list[index]))
                else:
                    result_scr.insert(tkinter.END,
                                      "匹配到 {}".format(keyword_list[index]))


# 创建主窗口
window = tkinter.Tk()

# 设置标题
window.title("配置查询")

# 设置窗口大小
window.geometry('400x700')

# 创建各组件文字标题
version_title = tkinter.Label(window, text='请选择系统', font=("宋体", 10, "normal"))
version_title['fg'] = 'black'
version_title.place(x=0, y=20, width=150, height=20)

game_title = tkinter.Label(window, text='请选择游戏', font=("宋体", 10, "normal"))
game_title['fg'] = 'black'
game_title.place(x=170, y=20, width=150, height=20)

versionnum_title = tkinter.Label(window,
                                 text='请输入版本号',
                                 font=("宋体", 10, "normal"))
versionnum_title['fg'] = 'black'
versionnum_title.place(x=0, y=80, width=150, height=20)

State = tkinter.Label(window, text='请选择地区后缀', font=("宋体", 10, "normal"))
State['fg'] = 'black'
State.place(x=170, y=80, width=150, height=20)

idfa_num = tkinter.Label(window, text='请输入idfa', font=("宋体", 10, "normal"))
idfa_num['fg'] = 'black'
idfa_num.place(x=0, y=130, width=150, height=20)

# 创建idfa输入框
idfa_input = tkinter.Variable()
idfa_input_num = tkinter.Entry(window, textvariable=idfa_input)
idfa_input_num.place(x=20, y=150, width=150, height=20)

# 创建地区选择下拉框
State_title = tkinter.StringVar()
State_choose = ttk.Combobox(window, width=12, textvariable=State_title)
State_choose['values'] = ('', '-US', '-CA', '-AU', '-FR', '-GB', '-DE', '-MX',
                          '-IT', '-ES', '-CL', '-TH', '-CO', '-RU', '-GE',
                          '-BR', '-PT', '-BE', '-SE', '-CZ', '-JP', '-AT',
                          '-CH', '-IN', '-PH')
State_choose['state'] = 'readonly'
State_choose.place(x=190, y=100, width=150, height=20)

# 创建系统选择下拉框
Version_sys = tkinter.StringVar()
Version_system = ttk.Combobox(window, width=12, textvariable=Version_sys)
Version_system['values'] = ('android', 'ios')
Version_system['state'] = 'readonly'
Version_system.place(x=20, y=40, width=150, height=20)
Version_system.current(0)

# 创建游戏选择下拉框
Object = tkinter.StringVar()
Object_game = ttk.Combobox(window, width=12, textvariable=Object)
Object_game['values'] = ('com.pixel.art.coloring.by.number',
                         'com.relax.coloring.games.color.by.number.colourpop',
                         'com.ball.brick.break',
                         'com.acoin.ballz.bricks.breaker')
Object_game['state'] = 'readonly'
Object_game.place(x=190, y=40, width=200, height=20)
Object_game.current(0)

# 创建输入文本框1--版本号输入
var_version = tkinter.Variable()
entry_version = tkinter.Entry(window, textvariable=var_version)
entry_version.place(x=20, y=100, width=150, height=20)

# 创建输入keyword输入框
var_keyword = tkinter.Variable()
keyword = tkinter.Entry(window, textvariable=var_keyword)
keyword.place(x=20, y=650, width=240, height=25)

# 创建关键字选择框1
keyword_sele = tkinter.StringVar()
keyword_select1 = ttk.Combobox(window, width=12, textvariable=keyword_sele)
keyword_select1.place(x=20, y=250, width=150, height=20)
keyword_select1['state'] = 'readonly'
keyword_select1.bind("<<ComboboxSelected>>", value_list_get)

# 创建关键字选择框2
keyword_sele2 = tkinter.StringVar()
keyword_select2 = ttk.Combobox(window, width=12, textvariable=keyword_sele2)
keyword_select2['state'] = 'readonly'
keyword_select2.place(x=190, y=250, width=150, height=20)
keyword_select2.bind("<<ComboboxSelected>>", value_result)

# 创建滚动文本框
result_scr = scrolledtext.ScrolledText(window,
                                       width=50,
                                       height=25,
                                       wrap=tkinter.WORD)
result_scr.place(x=20, y=310)

# 创建一个测试按钮
button_find = tkinter.Button(window,
                             text='查询',
                             bg='orange',
                             width=100,
                             height=50,
                             activebackground='orange',
                             activeforeground='white',
                             command=getinfo_By_textwin,
                             state="disabled")
button_find.place(x=280, y=650, width=100, height=25)

# 创建一个开始按钮
button = tkinter.Button(window,
                        text='开始',
                        bg='orange',
                        width=100,
                        height=50,
                        activebackground='orange',
                        activeforeground='white',
                        command=action_go)
button.place(x=150, y=185, width=100, height=50)

# 进入消息循环
window.mainloop()
