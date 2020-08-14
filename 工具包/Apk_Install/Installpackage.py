# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-07 17:11:07
# @Last Modified by:   Tommy
# @Last Modified time: 2020-04-29 16:52:41
import tkinter
import json
import adboperation
import os
import qrcode
from tkinter import ttk
from tkinter import scrolledtext
from ftpoperation import Ftpoperation


buffer_size = 8190
NoInternet = True


# 生成二维码的方法
def make_install_img():
    ip = data['GameChoosen'][game_name_box.get()]['FtpAddress']['ip']
    acct = data["GameChoosen"][game_name_box.get()]["FtpAddress"]["acct"]
    path = data['GameChoosen'][game_name_box.get(
    )]['android'][game_type_box.get()]
    apk_name = select_package_box.get()
    all_path = "http://" + ip + ':' + acct + '/' + path + '/' + apk_name
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1)
    qr.add_data(all_path)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('install_img.png')


# 获取安装包名称
def package_select(*args):
    # try:
    #     main()
    # except TimeoutError as e:
    #     result_scr.delete(1.0, tkinter.END)
    #     result_scr.insert(tkinter.END, '链接超时')
    if NoInternet:
        localapk_list = get_apk_by_local('包')
        select_package_box['values'] = list_key_select(localapk_list)
        select_package_box.current(0)


# json格式初始化
def json_data_init():
    # data = json_init()
    host = data["GameChoosen"][game_name_box.get()]["FtpAddress"]["ip"]
    user = data["GameChoosen"][game_name_box.get()]["FtpAddress"]["userName"]
    pwd = data["GameChoosen"][game_name_box.get()]["FtpAddress"]["Password"]
    acct = data["GameChoosen"][game_name_box.get()]["FtpAddress"]["acct"]
    return host, user, pwd, acct


# 数据变动，刷新的主要逻辑方法
def main():
    host, user, pwd, acct = json_data_init()
    # 实例化一个Ftpoperation对象类
    ftpobject = Ftpoperation(host, user, pwd, acct, buffer_size)
    # ftp链接
    ftpconnect, text = ftpobject.connect()
    result_scr.delete(1.0, tkinter.END)
    result_scr.insert(tkinter.END, text)

    # 判断是否登陆成功以确认后面的步骤
    if "失败" in text:
        result_scr.delete(1.0, tkinter.END)
        result_scr.insert(tkinter.END, text)
    else:
        # 定义重定向路径
        path = str(data["GameChoosen"][game_name_box.get()]
                   ["android"][game_type_box.get()])
        cwd_result = ftpobject.cwd_path(ftpconnect, path)
        if cwd_result:
            files = ftpconnect.nlst()  # 获取路径下文件或文件夹列表
            files.reverse()  # 简单的逆序
            if files:
                for file in files:
                    if ".apk" in file:
                        select_package_box['values'] = list_key_select(files)
                        select_package_box.current(0)
                        break
            else:
                select_package_box['values'] = "无参数"
                select_package_box.current(0)
        else:
            result_scr.delete(1.0, tkinter.END)
            result_scr.insert(tkinter.END, '不可以进入目录："%s"' % path + '请检查路径正确')
            select_package_box['values'] = 'NULL'
            select_package_box.current(0)
    ftpconnect.quit()


# 获取data参数的key值返回
def list_key_select(data):
    '''
    这里坐容错处理
    '''
    if type(data) == dict:  # 如果参数是个字典，返回list形式的key
        return list(data.keys())
    elif data:  # 不是dict就是list，可直接返回下拉框，下拉框直接接受list形式数据
        return data
    else:
        return "无参数"


# 读取json配置文件，返回dict
def json_init():
    with open('installConfig.json', 'r') as f:
        return json.load(f)


# 安装按钮绑定方法
def install_apk():
    if NoInternet:
        if "Success" in adboperation.install('包', select_package_box.get()):
            result_scr.delete(1.0, tkinter.END)
            result_scr.insert(tkinter.END, "安装成功")
        else:
            make_install_img()
            os.system('toplevel.exe')
    else:
        host, user, pwd, acct = json_data_init()
        ftpobject = Ftpoperation(host, user, pwd, acct, buffer_size)
        ftpconnect, text = ftpobject.connect()
        # 判断是否登陆成功以确认后面的步骤
        if "失败" in text:
            result_scr.delete(1.0, tkinter.END)
            result_scr.insert(tkinter.END, text)
        else:  # 连接成功，重定向到指定文件夹以下载apk
            path = str(data["GameChoosen"][game_name_box.get()]
                       ["android"][game_type_box.get()])
            ftpobject.cwd_path(ftpconnect, path)

            down_result = "重复安装"
            # 下载前需要检查本地 包 路径下是否存在要安装的包
            if not os.path.exists('包/' + select_package_box.get()):
                down_result = ftpobject.download(
                    ftpconnect, select_package_box.get())
            if down_result:
                result_scr.delete(1.0, tkinter.END)
                result_scr.insert(tkinter.END, down_result)

                # 下载成功后安装
                if "Success" in adboperation.install(
                        '包', select_package_box.get()):
                    result_scr.delete(1.0, tkinter.END)
                    result_scr.insert(tkinter.END, "安装成功")
                else:
                    make_install_img()
                    os.system('toplevel.exe')
            else:
                result_scr.delete(1.0, tkinter.END)
                result_scr.insert(tkinter.END, "下载失败,已移除失败apk文件")
                os.remove('包/' + select_package_box.get())


# 查询按钮绑定方法
def check_apk():
    tag = adboperation.inquiry_info(data["GameChoosen"]
                                    [game_name_box.get()]["PackageName"])
    result_scr.delete(1.0, tkinter.END)
    result_scr.insert(tkinter.END, tag)


# 重置内购包得安装方法
def resetPay():
    if "Success" in adboperation.install('包/TapColor_1.8.0.deal_order_1',
                                         'TapColor_1.8.0.deal_order_1.apk'):
        result_scr.delete(1.0, tkinter.END)
        result_scr.insert(tkinter.END, "安装成功，正在启动")
        adboperation.start_apk(
            "com.pixel.art.coloring.by.number", '.UnityPlayerActivity')
    else:
        result_scr.delete(1.0, tkinter.END)
        result_scr.insert(tkinter.END, "安装失败")


# 获取本地储存包list
def get_apk_by_local(path, suffixes=("apk"), traverse=False):
    """从path路径下，找出全部指定后缀名的文件

    :param path: 根目录
    :param suffixes: 指定查找的文件后缀名
    :param traverse: 如果为False，只遍历一层目录
    :return:
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_suffix = os.path.splitext(file)[1][1:].lower()   # 后缀名
            if file_suffix in suffixes:
                file_list.append(file)
        if not traverse:
            return file_list

    return file_list


# 创建主窗口
window = tkinter.Tk()

# 设置标题
window.title('安装APK应用')

# 设置窗口大小
window.geometry('400x450')

window.resizable(0, 0)  # 防止用户调整尺寸


# 创建各组件文字标题
game_name = tkinter.Label(window, text='请选择游戏名', font=("宋体", 10, "normal"))
game_name['fg'] = 'black'
game_name.place(x=60, y=20, width=52, height=14)

game_type = tkinter.Label(window, text='版本选择', font=("宋体", 10, "normal"))
game_type['fg'] = 'black'
game_type.place(x=290, y=20, width=52, height=14)

package_name = tkinter.Label(window, text='请选择安装包', font=("宋体", 10, "normal"))
package_name['fg'] = 'black'
package_name.place(x=161, y=84, width=78, height=14)

# 创建游戏名称选择下拉框
name_box = tkinter.StringVar()
game_name_box = ttk.Combobox(window, width=12, textvariable=name_box)
game_name_box.place(x=15, y=48, width=141, height=22)
game_name_box['state'] = 'readonly'
game_name_box.bind("<<ComboboxSelected>>", package_select)

# 创建游戏版本选择下拉框
tpye_box = tkinter.StringVar()
game_type_box = ttk.Combobox(window, width=12, textvariable=tpye_box)
game_type_box['values'] = ('debug', 'release')
game_type_box.place(x=245, y=48, width=141, height=22)
game_type_box.current(0)
game_type_box['state'] = 'readonly'
game_type_box.bind("<<ComboboxSelected>>", package_select)

# 创建安装包选择下拉框
select_package = tkinter.StringVar()
select_package_box = ttk.Combobox(
    window, width=12, textvariable=select_package, font=("宋体", 9, "normal"))
select_package_box['state'] = 'readonly'
select_package_box.place(x=15, y=112, width=371, height=22)

# 创建滚动文本框
result_scr = scrolledtext.ScrolledText(
    window, wrap=tkinter.WORD)
result_scr.place(x=15, y=173, width=371, height=101)

# 创建安装按钮
install_button = tkinter.Button(window,
                                text='安装',
                                bg='orange',
                                activebackground='orange',
                                activeforeground='white',
                                command=install_apk)
install_button.place(x=15, y=404, width=108, height=25)

# 创建查询按钮
check_button = tkinter.Button(window,
                              text='查询',
                              bg='orange',
                              activebackground='orange',
                              activeforeground='white',
                              command=check_apk)
check_button.place(x=278, y=404, width=108, height=25)

# 创建刷新按钮
refresh_button = tkinter.Button(window,
                                text='刷新apk列表',
                                bg='orange',
                                activebackground='orange',
                                activeforeground='white',
                                command=package_select)
refresh_button.place(x=147, y=404, width=108, height=25)

# 创建重置内购按钮
resetPay_button = tkinter.Button(window,
                                 text='重置内购',
                                 bg='orange',
                                 activebackground='orange',
                                 activeforeground='white',
                                 command=resetPay)
resetPay_button.place(x=147, y=369, width=108, height=25)

# 开始程序时，自动获取游戏名并赋值到组件内
data = json_init()
game_name_box['values'] = list_key_select(data["GameChoosen"])
game_name_box.current(0)

# try:
#     main()
# except TimeoutError as e:
#     localapk_list = get_apk_by_local('包')
#     select_package_box['values'] = list_key_select(localapk_list)
#     select_package_box.current(0)
#     NoInternet = True
if NoInternet:
    localapk_list = get_apk_by_local('包')
    select_package_box['values'] = list_key_select(localapk_list)
    select_package_box.current(0)


# 进入消息循环
window.mainloop()
