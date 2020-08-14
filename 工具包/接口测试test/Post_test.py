# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2020-03-20 18:11:13
# @Last Modified by:   Tommy
# @Last Modified time: 2020-03-20 18:34:07

# 引包
import requests
# 定义url
url = "http://ad.weplayer.cc/adInfo"
# 定义json格式
data = {"platform": "android", "packageName": "com.pixel.art.coloring.by.number",
        "versionCode": 119, "idfa": 1}
# 定义headers
headers = {"Content-type": "application/json", "Accept": "text/plain"}
# 调用 Post方法-------json参数
r = requests.post(url, json=data, headers=headers)
# 调用 Post方法-------data参数
# r = requests.post(url, data=data, headers=headers)
# 获取响应数据----json形式
print(r.json())
# 获取响应数据----text形式
print(r.text)
'''
    Post请求中，参数data和json的区别：
        python中，字典和json长得一样，但是数据序列化格式还是有一定区别的
        可以强制转换： data = json.dumps(dict)

    Post的响应对象，.json和.text的区别：
        只是长得很像
        .json形式返回值类型为：dict
        .text形式返回值类型为：str
'''
