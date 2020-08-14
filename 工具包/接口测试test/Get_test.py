# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2020-03-20 11:20:57
# @Last Modified by:   Tommy
# @Last Modified time: 2020-03-20 15:15:59

# 引包
import requests

# 参数化url
url = "http://www.baidu.com"
# get方法带参数
# params = {"id": 1001}
# params = {"id": "1001, 1002"}  ------> %2c 为ASCI码的逗号
params = {"id": 1001, "kw": "北京"}
# get方法访问url，返回response对象
response = requests.get(url, params=params)

# 获取响应对象相应信息： 响应对象.url/响应对象.status_code/响应对象.text
print("请求地址", response.url)
print("状态码", response.status_code)
print("文本响应内容", response.text)
