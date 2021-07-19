'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-07-19 18:11:13
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-07-19 18:13:44
'''
import requests


class Request():
    def request_get(self, url, parm):
        res = requests.get(url=url, params=parm)
        return res