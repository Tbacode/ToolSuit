'''
 * @Descripttion : 退出按钮验证
 * @Author       : Tommy
 * @Date         : 2020-12-15 18:35:19
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-15 18:41:37
'''
import tkinter as tk
from tkinter.messagebox import askokcancel


class Quitter(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        widget = tk.Button(self, text='Quit', command=self.quit)
        widget.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans:
            tk.Frame.quit(self)


if __name__ == "__main__":
    Quitter().mainloop()
