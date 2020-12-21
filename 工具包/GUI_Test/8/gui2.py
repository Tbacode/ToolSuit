'''
 * @Descripttion : gui学习第二章
 * @Author       : Tommy
 * @Date         : 2020-12-03 18:11:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-21 12:19:29
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
'''
    虽然Toplevel是独立活动得窗口，但是他们不是单独得进程；
    如果用户得程序终止，那么该程序得所有窗口都会消失，包括所有可能已经创建得Toplevel窗口
    之后会通过独立得GUI程序绕开这个规则。
'''

# import sys
# from tkinter import Toplevel, Button, Label
# win1 = Toplevel()
# win2 = Toplevel()

# Button(win1, text='Spam', command=sys.exit).pack()
# Button(win2, text='SPAM', command=sys.exit).pack()

# Label(text='Popups').pack()
# win1.mainloop()


# Toplevel组件和TK组件
# import tkinter
# from tkinter import Tk, Button
# tkinter.NoDefaultRoot()

# win1 = Tk()
# win2 = Tk()

# Button(win1, text="spam", command=win1.destroy).pack()
# Button(win2, text="SPAM", command=win2.destroy).pack()

# win1.mainloop()

# 顶层窗口协议

# from tkinter import *
# root = Tk()

# trees = [('The Larch!', 'light blue'),
#          ('The Pine!', 'light green'),
#          ('The Giant Redwood!', 'red')
#          ]
# for (tree, color) in trees:
#     win = Toplevel(root)
#     win.title('Sing...')
#     win.protocol('WM_DELETE_WINDOW', lambda: None) # 忽略关闭按钮
#     # win.iconbitmap('py-blue-trans-out.ico')

#     msg = Button(win, text=tree, command=win.destroy)
#     msg.pack(expand=YES, fill=BOTH)
#     msg.config(padx=10, pady=10, bd=10, relief=RAISED)
#     msg.config(bg='black', fg=color, font=('times', 30, 'bold italic'))

# root.title('Lumberjack demo')
# Label(root, text='Main window', width=30).pack()
# Button(root, text='Quit All', command=root.quit).pack()
# root.mainloop()


# 对话框


'''
模态：
    这种对话框会阻止其他界面，直到对话框被关闭；
    想要程序继续进行，用户必须对 对话框做出回应
非模态：
    这种对话框可以永久停留在屏幕上，而不会干扰界面中得其他窗口；
    这种对话框常常可以随时接受输入
'''
# 标准（通用）对话框
# 标准对话框调用都是模态的，而且标准对话框在显示的时候，阻塞了程序的主窗口


# from tkinter import *
# from tkinter.messagebox import *
# def callback():
#     if askyesno('Verify', 'Do you really want to quit?'):
#         showwarning('Yes', 'Quit not yet implemented')
#     else:
#         showinfo('No', 'Quit has been cancelled')


# errmsg = 'Sorry, no Spam allowed'
# Button(text='Quit', command=callback).pack(fill=X)
# Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
# mainloop()

# 可复用的Quit按钮
'''
验证退出请求的Quit按钮
复用、链接其他GUI的实例，并按需求重新封装
'''
# from tkinter import *
# from tkinter.messagebox import askokcancel
# class Quitter(Frame):
#     def __init__(self, parent=None):
#         Frame.__init__(self, parent)
#         self.pack()
#         widget = Button(self, text='Quit', command=self.quit)
#         widget.pack(side=LEFT, expand=YES, fill=BOTH)

#     def quit(self):
#         ans = askokcancel('Verify exit', "Really quit?")
#         if ans:
#             Frame.quit(self)


# if __name__ == "__main__":
#     Quitter().mainloop()


# 对话框演示启动栏
'''
创建一个简单的按钮栏，弹出对话框演示，引用dialogTable.py
'''


from tkinter import *
from dialogTable import demos
from quitter import Quitter
class Demo(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack()
        Label(self, text="Basic demos").pack()
        # for (key, value) in demos.items():
        for key in demos:
            func = (lambda key=key: self.printit(key))
            Button(self, text=key, command=func).pack(side=TOP, fill=BOTH)
        Quitter(self).pack(side=TOP, fill=BOTH)
    
    def printit(self, name):
        print(name, 'returens =>', demos[name]())


if __name__ == "__main__":
    Demo().mainloop()
