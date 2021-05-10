'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-01-07 17:15:33
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-04-20 18:44:08
'''
import xlrd
from xlutils.copy import copy


class Excel_operation(object):
    def __init__(self, filename):
        self.filename = filename

    # TODO: 打开excel文件
    def excel_open(self):
        excel_object = xlrd.open_workbook(self.filename)
        return excel_object

    # TODO: 获取表对象
    def get_table_by_sheetname(self, excel_object, sheet_name: str):
        table = excel_object.sheet_by_name(sheet_name)
        return table

    # TODO: 返回表的行数
    def get_table_rows(self, table_object):
        return table_object.nrows

    # TODO: 返回表的列数
    def get_table_cols(self, table_object):
        return table_object.ncols

    # TODO: excel单元格数据返回
    def excel_celldata_return(self, row, col, table_object):
        return table_object.cell_value(row, col)

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