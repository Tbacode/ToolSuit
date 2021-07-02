'''
 * @Descripttion : 封装request基础类
 * @Author       : Tommy
 * @Date         : 2021-06-17 10:52:32
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-07-02 13:19:20
'''
import requests
import json
import sys
sys.path.append("..")
from Util.handle_ini import handle_ini


class BaseRequest(object):
    def __send_post(self, url, data):
        '''
         * @name: Tommy
         * @msg: 私有化封装post请求
         * @param {url:请求地址,data:请求参数}
         * @return {请求结果}
        '''
        res = requests.post(url=url, data=data).text
        return res

    def __send_get(self, url, data):
        '''
         * @name: Tommy
         * @msg: 私有化封装get请求
         * @param {url:请求地址,data:请求参数}
         * @return {请求结果}
        '''
        res = requests.get(url=url, params=data).text
        return res

    def run_main(self, method, url, data):
        '''
         * @name: Tommy
         * @msg: 运行函数main
         * @param {method:请求方式,url:请求地址,data:请求参数}
         * @return {请求结果}
        '''
        # base_url = handle_ini.get_ini_value(ini_hostkey)
        # url = base_url + url
        # print(url)
        if method == 'get':
            res = self.__send_get(url, data)
        else:
            res = self.__send_post(url, data)
        try:
            res = json.loads(res)
        except Exception:
            print("这个结果是一个text")
        return res


request = BaseRequest()
# if __name__ == "__main__":
#     re = BaseRequest()
#     re.run_main('get', '/normalApi/v1/getBannerConfig/', 'sdf', 'colorhost')
