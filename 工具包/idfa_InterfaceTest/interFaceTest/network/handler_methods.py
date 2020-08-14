# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-06-26 14:49:57
# @Last Modified by:   Tommy
# @Last Modified time: 2020-04-08 18:39:45

"""
服务端 json格式
"""
import requests
import ujson


class HandlerMethods():

    HEADER = None

    def set_new_headers(self, header_data: dict):
        """
        新版设置头
        获取头用 getattr
        :param header_data:
        :return:
        """
        setattr(HandlerMethods, "HEADER", header_data)

    def check_headers(self, res):
        """
        检查包头内容 只能用于基础查询 如果要用这个得用最基础写法 不能用do_method_v1和do_post
        hasattr 不想用的话改为 if obj in objGroup模式也行
        :param res:res = requests.post(url)或者get插入部分
        :return:
        """
        setattr(HandlerMethods, "HEADER", res.headers["Content-Type"])

    def do_method_reflect(self, url, method: str = "GET", data=None):
        """
        万能requests
        支持发送方式 get post put
        :param url:地址
        :param method:
        :param data:
        :param encoding:
        :return:
        """
        method = method.strip().lower() if hasattr(requests, method) else "get"
        func = getattr(requests, method)
        if method in ['post', 'put']:
            print("执行post分支")
            try:
                res = func(url, data)
            except:
                print("超时")
                return False
        else:
            print("执行get分支")
            try:
                res = func(url, params=data)
            except:
                print("超时")
                return False
            else:
                self.check_headers(res)  # 获取新的包头

        return res

    def request_task(self, url, parms, check_parm, method: str = "GET"):
        """
        发送任务
        :param url:
        :return: 
        """
        flag = True
        if method == "post":
            # check_parm = ujson.loads(parms)
            parms = ujson.loads(parms)
        res = self.do_method_reflect(url, method, parms)
        if res:
            if method == "post":
                res = self.get_ujson_info(res)
                # print(type(eval(res)))
                for check_parm_item in eval(check_parm):
                    if check_parm_item not in res:
                        print("无效匹配:{}".format(check_parm_item))
                        flag = False
                return flag
            return True if res.status_code == 200 else False
        else:
            return False
