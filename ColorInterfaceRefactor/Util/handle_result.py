'''
 * @Descripttion : 处理预期结果
 * @Author       : Tommy
 * @Date         : 2021-06-29 17:13:29
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-30 15:02:10
'''
from Util.handle_json import get_value
from deepdiff import DeepDiff


def handle_result(url, filepath, code):
    '''
     * @name: Tommy
     * @msg: 获取本地errorMsg的json文件
     * @param {url:请求url,filepath:json路径,code:errorCode值}
     * @return {返回对应的errorMsg或None}
    '''
    res_list = get_value(url, filepath)
    if res_list is not None:
        for item in res_list:
            message = item.get(str(code))
            if message is not None:
                return message
    return None


def handle_result_json(dict1, dict2):
    '''
     * @name: Tommy
     * @msg: dict格式对比验证
     * @param {dict1:验证dict参数1,dict2:验证dict参数2}
     * @return {bool}
    '''
    cmp_dict = DeepDiff(dict1, dict2, ignore_order=True).to_dict()
    if cmp_dict.get("dictionary_item_added"):
        return False
    else:
        return True


if __name__ == '__main__':
    p = handle_result("/normalApi/v1/getBannerConfig/",
                      r"../Config/check_config.json", "666")
    print(p)
