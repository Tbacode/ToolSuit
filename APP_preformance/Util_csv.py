'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-10-15 12:05:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-10-20 16:02:47
'''
import csv


class UsingMyCsv(object):

    def __init__(self, path: str) -> None:
        self._csv_path = path

    def get_data(self):
        with open(self._csv_path, 'r', encoding='utf-8') as fp:
            lines = csv.reader(fp)
            for line in lines:
                yield line
