'''
 * @Descripttion : 回调演示表
 * @Author       : Tommy
 * @Date         : 2020-12-15 18:27:53
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-15 18:33:24
'''
from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import askcolor
from tkinter.messagebox import askquestion, showerror
from tkinter.simpledialog import askfloat

demos = {
    'Open': askopenfilename,
    'Color': askcolor,
    'Query': lambda: askquestion('Warning', 'You typed "rm *"\nConfirm?'),
    'Error': lambda: showerror('Error!', "He's dead, Jim"),
    'Input': lambda: askfloat('Entry', 'Enter credit card number')
}
