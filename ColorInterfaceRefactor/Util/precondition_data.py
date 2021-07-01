'''
 * @Descripttion : 前置条件的预处理
 * @Author       : Tommy
 * @Date         : 2021-07-01 14:32:09
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-07-01 17:14:07
'''
from Util.handle_excel import excel
from jsonpath_rw import parse
import json


def split_data(data):
    '''
     * @name: Tommy
     * @msg: 解析从excel来的前置条件数据
     * @param {data:excel中的Precondition数据}
     * @return {返回caseID,解析规则数据}
    '''
    case_id = data.split(">")[0]
    rule_data = data.split(">")[1]
    return case_id, rule_data


def depend_data(data, key, Response_Result_index, index=None):
    '''
     * @name: Tommy
     * @msg: 返回对应依赖数据结果集
     * @param {data:前置条件数据, key:表格列关键字, Response_Result_index:结果回写索引, index:表索引}
     * @return {返回对应单元格数据}
    '''
    case_id, rule_data = split_data(data)
    row = excel.get_row_number(case_id, key, index)
    cell_data = excel.get_cell_value(row, Response_Result_index + 1, index)
    return eval(cell_data), rule_data


def get_depend_data(depend_data, depend_rule):
    '''
     * @name: Tommy
     * @msg: 根据依赖数据获取依赖字段
     * @param {depend_data:依赖数据, depend_rule:依赖规则}
     * @return {返回对应的依赖字段数值}
    '''
    json_exe = parse(depend_rule)
    madle = json_exe.find(depend_data)
    return [math.value for math in madle][0]
