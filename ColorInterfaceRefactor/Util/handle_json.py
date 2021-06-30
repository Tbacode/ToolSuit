'''
 * @Descripttion : json文件处理
 * @Author       : Tommy
 * @Date         : 2021-06-29 17:16:38
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-30 15:10:45
'''
import json


def read_json(path):
    '''
     * @name: Tommy
     * @msg: 打开json文件
     * @param {path:文件路径}
     * @return {返回字符串对象}
    '''    
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_value(key, path):
    '''
     * @name: Tommy
     * @msg: 获取key对应json内容
     * @param {key:key值,path:文件路径}
     * @return {返回获取的值}
    '''    
    data = read_json(path)
    return data.get(key)
    