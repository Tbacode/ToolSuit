'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-01-05 18:49:23
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-05 18:54:42
'''
import sys


def fun1(aaa):
    if aaa:
        print("进来了")

    else:
        print("出来了")


if __name__ == "__main__":
    aaa = sys.argv[1]
    fun1(bool(aaa))
