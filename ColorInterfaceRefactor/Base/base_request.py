'''
 * @Descripttion : 封装request基础类
 * @Author       : Tommy
 * @Date         : 2021-06-17 10:52:32
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-25 16:14:02
'''
import requests
import json
import sys
sys.path.append("..")
from Util.handle_ini import handle_ini
from loguru import logger


class BaseRequest(object):
    def __send_post(self, url, data):
        '''
         * @name: Tommy
         * @msg: 私有化封装post请求
         * @param {url:请求地址,data:请求参数}
         * @return {请求结果}
        '''
        i = 0
        while i<5:
            try:
                logger.debug("请求开始，url:" + url)
                res = requests.post(url=url, data=data).text
                return res
            except requests.exceptions.RequestException:
                logger.error("请求超时20s，重试...")
                i += 1
        return None

    def __send_get(self, url, data):
        '''
         * @name: Tommy
         * @msg: 私有化封装get请求
         * @param {url:请求地址,data:请求参数}
         * @return {请求结果}
        '''
        # res = requests.get(url=url, params=data)
        # print(res.url)
        i = 0
        while i < 5:
            try:
                logger.debug("请求开始，url:" + url)
                res = requests.get(url=url, params=data, timeout=10).text
                return res
            except requests.exceptions.RequestException:
                logger.error("请求超时20s，重试...")
                i += 1
        return None

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
            logger.error("请求超时，结果为空")
            return {"errorMsg": "请求超时，结果为空", "errorCode": 555}
        return res


request = BaseRequest()
# if __name__ == "__main__":
#     re = BaseRequest()
#     re.run_main('get', '/normalApi/v1/getBannerConfig/', 'sdf', 'colorhost')
