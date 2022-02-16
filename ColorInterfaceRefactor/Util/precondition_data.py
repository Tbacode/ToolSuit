'''
 * @Descripttion : 前置条件的预处理
 * @Author       : Tommy
 * @Date         : 2021-07-01 14:32:09
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-25 16:02:01
'''
from Util.handle_excel import excel
from jsonpath_rw import parse
# from Cryptodome.Cipher import AES
# import base64


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

def split_data_by_ExpectedResult(data):
    '''
     * @name: Tommy
     * @msg: 解析从excel来的预期结果数据
     * @param {data:excel中Expected Result数据}
     * @return {返回解析规则数据, 运算符, 预期结果数据}
    '''
    rule_data_result, operator, expectedresult = data.split("@")
    return rule_data_result, operator, expectedresult

def get_result_check(depend_data, operator, expectedresult):
    '''
     * @name: Tommy
     * @msg: 
     * @param {*} depend_data    依赖规则解析后的依赖数据
     * @param {*} operator       运算符号
     * @param {*} expectedresult 预期结果，与以来数据进行运算判定
     * @return {boolean} 返回真假
    '''
    if operator == "!=":
        if int(depend_data) != int(expectedresult):
            return True
    elif operator == "<=":
        if int(depend_data) <= int(expectedresult):
            return True
    elif operator == "=":
        if int(depend_data) == int(expectedresult):
            return True
    elif operator == ">=":
        if int(depend_data) >= int(expectedresult):
            return True
    elif operator == "<":
        if int(depend_data) < int(expectedresult):
            return True
    elif operator == ">":
        if int(depend_data) > int(expectedresult):
            return True
    elif operator == "NotIn":
        if str(depend_data) not in str(expectedresult):
            return True
    elif operator == "In":
        if str(depend_data) in str(expectedresult):
            return True
    else:
        return False
    


def depend_data(data, key, Response_Result_index, index=None):
    '''
     * @name: Tommy
     * @msg: 返回对应依赖数据结果集
     * @param {data:前置条件数据, key:表格列关键字, Response_Result_index:结果回写索引, index:表索引}
     * @return {返回对应单元格数据, 规则字符串}
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


# def AES_Decrypt(key, data):
#     def unpad(s):
#         return s[0:-s[-1]]

#     data = data.encode('utf8')
#     # 将加密数据转换位bytes类型数据
#     encodebytes = base64.b64decode(data)
#     vi = encodebytes[:16]
#     test_encodebytes = encodebytes[16:]
#     cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi)

#     text_decrypted = cipher.decrypt(test_encodebytes)

#     text_decrypted = unpad(text_decrypted)
#     text_decrypted = text_decrypted.decode('utf8')
#     return text_decrypted

if __name__ == "__main__":

    text = AES_Decrypt("talefuntapcolor!", "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")
    print(text)