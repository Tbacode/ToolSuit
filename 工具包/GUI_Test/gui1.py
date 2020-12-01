'''
Descripttion: guitest
Author: Tommy
Date: 2020-10-26 16:34:19
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-11-25 14:47:10
'''
# from tkinter import Label
# widget = Label(None, text='hello GUI world!')
# widget.pack()
# widget.mainloop()

# 重写上述代码
# from tkinter import *
# Label(text="hello GUI world!").pack()
# mainloop()

# 调整窗口内居中且适应窗口大小调整
# from tkinter import *
# expand选项允许打包几何管理器为组件扩展空间，通常可以是父组件中未被占用的地方
# fill选项允许是否可用来拉伸组件，使其充满分配的空间
# Label(text="hello GUI world!").pack(expand=YES, fill=BOTH)
# mainloop()

# 调用组件的config方法来进行组件选项设置
# from tkinter import *
# root = Tk()
# widset = Label(root)
# widset.config(text='Hello GUI world!')
# widset.pack(side=TOP, expand=YES, fill=BOTH)
# root.title('gui.py')
# root.mainloop()
'''
    pack()返回的是空对象，任何pack的链式调用均会异常
    eg: widset = Lable(text='hi').pack()
        Lable(text='hi').pack().mainloop()
'''

# 添加按钮和回调函数
# import sys
# from tkinter import *
# root = Tk()
# widset = Button(root, text='Exit', command=root.quit)
# widset.pack()
# root.mainloop()

# 按钮的扩展
# from tkinter import *
# root = Tk()
# widset = Button(root, text='exit', command=root.quit)
# widset.pack(side=LEFT, expand=YES, fill=X)
# root.mainloop()

# 自定义函数绑定button，lambda函数
# from tkinter import *
# root = Tk()
# Widget = Button(root,
#                 text='exit',
#                 command=(lambda: print("hello lambda world") or root.quit()))
# Widget.pack()
# root.mainloop()
'''
button中回调处理器需要的状态信息必须以其他形式提供
lambda函数将button的command函数映射到另一个由lambda提供的带参函数上，处理回调延迟

'''
# 打包延迟
'''
延迟的必要性在于，如果在按钮创建函数中加入处理器调用，而没有采用lambda或其他中间函数
回调会发生在 #按钮创建时#，而不是之后的按钮点击时。
这就是为什么要用中间函数来屏蔽回调，以延迟触发
'''
# from tkinter import *

# def handler(name):
#     print(name)

# root = Tk()
# # Widget = Button(root, text='Exit', command=handler('tommy'))
# Widget = Button(root, text='Exit', command=lambda: handler('tommy'))
# Widget.pack()
# root.mainloop()

# bound方法回调处理器
# import sys
# from tkinter import *


# class HelloClass:
#     def __init__(self):
#         widset = Button(None, text="exit", command=self.quit)
#         widset.pack()

#     def quit(self):
#         print("Exit....")
#         sys.exit()


# HelloClass()
# mainloop()

# 可调用类对象的回调处理器


# from tkinter import *
# import sys
# class HelloCallable:
#     def __init__(self):
#         self.msg = 'hello __call__ world'

#     def __call__(self):
#         print(self.msg)
#         sys.exit()


# Widget = Button(None, text='hello event world', command=HelloCallable())
# Widget.pack()
# Widget.mainloop()

# 多组件加入
# from tkinter import *

# def greeting():
#     print('Hello stdout world!..')

# win = Frame()
# win.pack()
# Label(win, text='Hello container world').pack(side=TOP)
# Button(win, text='Hello', command=greeting).pack(side=LEFT)
# Label(win, text='Hello container world').pack(side=TOP)
# Button(win, text='Quit', command=win.quit).pack(side=RIGHT)
# Label(win, text='Hello container world').pack(side=TOP)
'''
    TIP：先打包的组件总是最后消失，
    eg：尽管Label的布局位于top，但是窗口缩小时，只有打包顺序会影响布局
'''

# win.mainloop()

# packer的expand和fill选项
# from tkinter import *

# def greeting():
#     print("hello world")

# win = Frame()
# win.pack(side=TOP, expand=YES, fill=BOTH)
# Button(win, text='Hello', command=greeting).pack(side=LEFT, SSSfill=Y)
# Label(win, text='Hello container world').pack(side=TOP)
# Button(win, text='Quit', command=win.quit).pack(side=RIGHT, expand=YES, fill=X)

# win.mainloop()




from tkinter import *
class ThemeButton(Button):
    """
    自定义button类
    """

    def __init__(self, parent=None, **configs):
        Button.__init__(self, parent, **configs)
        self.pack()
        self.config(fg='red', bg='black', font=(
            'courier', 12), relief=RAISED, bd=5)

B1 = ThemeButton(text='spam', command=onSpam)
B2 = ThemeButton(text='eggs')
B2.pack(expand=YES, fill=BOTH)
