# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-15 10:47:37
# @Last Modified by:   Tommy
# @Last Modified time: 2019-05-15 13:53:35
from PIL import Image, ImageTk
import tkinter

window = tkinter.Tk()
window.title('扫码安装')

img_open = Image.open('install_img.png')
img_png = ImageTk.PhotoImage(img_open)
label_img = tkinter.Label(window, image=img_png)
label_img.pack()

window.mainloop()
