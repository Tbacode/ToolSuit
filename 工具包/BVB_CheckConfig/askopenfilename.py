'''
@Descripttion: 11
@Author: Tommy
@Date: 2020-07-22 18:52:44
@LastEditors: Tommy
@LastEditTime: 2020-07-30 15:01:07
'''
# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2020-07-22 18:52:44
# @Last Modified by:   Tommy
# @Last Modified time: 2020-07-22 18:54:15

# import tkinter
# from tkinter import filedialog

# root = tkinter.Tk()

# filePath = filedialog.askdirectory()
# print(filePath)
# import json

# with open("config.json", "rb") as f:
#     res = json.load(f)
# res["noDownBlock"].append(-11)
# with open("config.json", "w+", encoding='utf-8') as a:
#     json.dump(res, a, ensure_ascii=False)
import datetime

now = datetime.datetime.now()
delta = datetime.timedelta(days=2)
n_days = now + delta
print(n_days.strftime('%Y%m%d'))
