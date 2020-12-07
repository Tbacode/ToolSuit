'''
 * @Descripttion : gui学习第二章
 * @Author       : Tommy
 * @Date         : 2020-12-03 18:11:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-04 10:25:35
'''
# 配置组件外观

# from tkinter import *
# root = Tk()
# # 定义字体的元组参数集，字体，大小，类型(normal，bold, romam, italc, underline, overstrike及它们结合)
# labelfont = ('times', 20, 'bold')
# Widget = Label(root, text='Hello config world')
# Widget.config(bg='black', fg='yellow')
# Widget.config(font=labelfont)
# Widget.config(height=3, width=20)  # 定义行间距，字符间距
# Widget.pack()
# root.mainloop()


# 其余组件设置参数

# from tkinter import *
# Widget = Button(text='Spam', padx=10, pady=10)  # pad参数留白
# Widget.pack(padx=20, pady=20)
# Widget.config(cursor='gumby')  # 光标
# Widget.config(bd=8, relief=RAISED)  # 设定边框宽度和边框类型
# Widget.config(bg='dark green', fg='white')
# Widget.config(font=('helvetica', 20, 'underline italic'))
# mainloop()


# 顶层窗口

import sys
from tkinter import Toplevel, Button, Label

win1 = Toplevel()
win2 = Toplevel()

Button(win1, text='Spam', command=sys.exit).pack()
Button(win2, text='SPAM', command=sys.exit).pack()

Label(text='Popups').pack()
win1.mainloop()
