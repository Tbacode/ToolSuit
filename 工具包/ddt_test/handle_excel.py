'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-01-07 17:15:33
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-04-20 19:17:35
'''
import openpyxl
from xlutils.copy import copy


class HandleExcel(object):
    def __init__(self, filename):
        self.filename = filename

    # TODO: 打开excel文件
    def excel_open(self):
        excel_object = openpyxl.load_workbook(self.filename)
        return excel_object

    # TODO: 获取表对象
    def get_table_by_index(self, index=None):
        sheet_name = self.excel_open().sheetnames
        if index is None:
            index = 0
        data = self.excel_open()[sheet_name[index]]
        return data

    # TODO: 返回表的行数
    def get_table_rows(self, table_object):
        return table_object.nrows

    # TODO: 返回表的列数
    def get_table_cols(self, table_object):
        return table_object.ncols

    # TODO: excel单元格数据返回
    def get_cell_value(self, row, col, index=None):
        return self.get_table_by_index(index).cell(row=row, column=col).value

    # TODO: excel追加数据
    def excel_celldata_add(self, row, col, sheet_name, content):
        # 打开表格
        excel_object = self.excel_open()
        # 将xlrd对象转换成xlwt对象
        xlwt_object = copy(excel_object)
        # 获取写入对象表
        table_object = xlwt_object.get_sheet(sheet_name)
        # 追加内容到单元格
        table_object.write(row, col, content)
        # 保存并覆盖
        xlwt_object.save(self.filename)