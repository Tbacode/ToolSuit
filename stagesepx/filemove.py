'''
 * @Description  : 移动文件
 * @Autor        : Tommy
 * @Date         : 2021-03-13 14:41:22
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-03-13 18:48:34
'''
import os
import tkinter
from tkinter import scrolledtext
from tkinter import END
import shutil
from loguru import logger


def Start():
    path = './stable_frame'
    sourceDir = os.path.join(path, source_input.get())
    targetDir = os.path.join(path, target_input.get())
    result_scr.insert(tkinter.END, "----Start----" + "\n")
    result_scr.see(END)
    result_scr.update()
    filemove(targetDir, sourceDir)


def filemove(targetDir: str, sourceDir: str) -> None:
    for root, dirs, files in os.walk(sourceDir):
        for file in files:
            logger.debug("合并文件路径：{}".format(os.path.join(sourceDir, file)))
            shutil.move(os.path.join(sourceDir, file), targetDir)
    os.rmdir(sourceDir)
    result_scr.insert(tkinter.END, "----End----" + "\n")
    result_scr.see(END)
    result_scr.update()


# 创建主窗口
window = tkinter.Tk()

# 设置标题
window.title("文件移动")

# 设置窗口大小
window.geometry('610x700')

# 创建各组件文字标题
target_Label = tkinter.Label(window, text='目标文件目录', font=("宋体", 10, "normal"))
target_Label['fg'] = 'black'
target_Label.place(x=0, y=0, width=85, height=25)

# target 输入框
target_txt = tkinter.Variable()
target_input = tkinter.Entry(window, textvariable=target_txt)
target_input.place(x=10, y=35, width=250, height=25)

source_Label = tkinter.Label(window, text='來源文件目录', font=("宋体", 10, "normal"))
source_Label['fg'] = 'black'
source_Label.place(x=0, y=70, width=85, height=25)

# source 输入框
source_txt = tkinter.Variable()
source_input = tkinter.Entry(window, textvariable=source_txt)
source_input.place(x=10, y=105, width=250, height=25)

# 创建一个开始按钮
button = tkinter.Button(window,
                        text='开始移动',
                        bg='orange',
                        activebackground='orange',
                        activeforeground='white',
                        command=Start)
button.place(x=400, y=55, width=80, height=50)

# 创建一个滚动文本框
result_scr = scrolledtext.ScrolledText(window,
                                       width=80,
                                       height=20,
                                       wrap=tkinter.WORD)
result_scr.place(x=20, y=140)

# 进入主循环
window.mainloop()