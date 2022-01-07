'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-01-05 15:04:59
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-05 15:04:59
'''

from sqlalchemy import create_engine

# 准备链接
engine = create_engine('mysql://root:3232636521tuot@127.0.0.1:3306/learn_orm?charset=utf8',
                       echo=True)