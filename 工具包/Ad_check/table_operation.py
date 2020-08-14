# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-07-05 17:13:42
# @Last Modified by:   Tommy
# @Last Modified time: 2019-07-24 11:55:55
import xlrd
import os
import json


class Table_Operation(object):
    """封装对于查表相关操作"""
    def check_IsABGroup():
        '''检查表中参数是否有分组信息'''
        worksheet = xlrd.open_workbook("Tapcolor-IOS测试.xlsx")
        sheet_names = worksheet.sheet_names()
        sheet = worksheet.sheet_by_name(sheet_names[0])
        cols = sheet.col_values(2)
        print(set(cols))
        if len(set(cols)) > 1:
            return True

    def get_adInfo_fromAdType(file_path, ad_type):
        r_xls = xlrd.open_workbook(file_path)
        table = r_xls.sheets()[0]
        i = 0
        re_type_list_A = []
        re_type_list_B = []
        try:
            while table.cell(i, 0).ctype != 0:
                flag = {}
                if table.cell(i, 6).value.lower() == ad_type:
                    if 'A' in table.cell(i, 2).value:
                        if table.cell(i, 0).ctype == 2 and table.cell_value(i, 0) % 1 == 0:
                            # re_type_list_A.append(
                            #     str(int(table.cell(i, 0).value)))
                            flag["adID"] = str(int(table.cell(i, 0).value))
                            flag["channel"] = str(table.cell(i, 3).value)
                            re_type_list_A.append(flag)
                        else:
                            # re_type_list_A.append(str(table.cell(i, 0).value))
                            flag["adID"] = str(table.cell(i, 0).value)
                            flag["channel"] = str(table.cell(i, 3).value)
                            re_type_list_A.append(flag)
                    else:
                        if table.cell(i, 0).ctype == 2 and table.cell_value(i, 0) % 1 == 0:
                            # re_type_list_B.append(
                            #     str(int(table.cell(i, 0).value)))
                            flag["adID"] = str(int(table.cell(i, 0).value))
                            flag["channel"] = str(table.cell(i, 3).value)
                            re_type_list_B.append(flag)
                        else:
                            # re_type_list_B.append(str(table.cell(i, 0).value))
                            flag["adID"] = str(table.cell(i, 0).value)
                            flag["channel"] = str(table.cell(i, 3).value)
                            re_type_list_B.append(flag)
                i += 1
        except IndexError:
            pass
        print(json.dumps(re_type_list_A, indent=1))
        print("--------------")
        print(json.dumps(re_type_list_B, indent=1))
        return re_type_list_A, re_type_list_B

    def get_excel_object(suffixes=("xlsx"), traverse=False):
        '''遍历当前脚本路径下查找excel文件并返回绝对路径'''
        path = os.path.split(os.path.realpath(__file__))[0]
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_suffix = os.path.splitext(file)[1][1:].lower()   # 后缀名
                if file_suffix in suffixes:
                    file_list.append(os.path.join(root, file))
            if not traverse:
                return file_list

        return file_list


if __name__ == '__main__':
    if Table_Operation.check_IsABGroup():
        print(Table_Operation.get_adInfo_fromAdType(
            r'C:\Users\xt875\Desktop\脚本\Ad_check\Tapcolor-IOS测试.xlsx', 'banner'))
