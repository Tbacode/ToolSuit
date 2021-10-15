'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-10-15 12:05:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-10-15 12:10:48
'''
import csv


class UsingMyCsv(object):

    def __init__(self, path: str) -> None:
        self._csv_path = path

    def get_data(self):
