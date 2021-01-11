'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2020-12-21 14:23:04
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-21 14:26:05
'''
from tkinter import *
from tkinter.colorchooser import askcolor

def setBgcolor():
    (triple, hexstr) = askcolor()
    if hexstr:
        print(hexstr)
        push.config(bg=hexstr)

root = Tk()
push = Button(root, text='Set Background Color', command=setBgcolor)
push.config(height=3, font=('times', 20, 'bold'))
push.pack(expand=YES, fill=BOTH)
root.mainloop()