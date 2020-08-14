# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2020-03-31 15:41:52
# @Last Modified by:   Tommy
# @Last Modified time: 2020-03-31 16:20:29
'''
    response.status_code        状态码
    response.url                请求url
    response.encoding           查看响应头部字符编码
    response.headers            头信息
    response.cookies            cookie信息
    response.text               文本形式响应内容
    response.content            字节形式响应内容(图片，视频。。。多媒体格式)
    response.json()             json形式响应内容
'''
# 引包
import requests

# 调用get方法
url = "http://www.baidu.com"
response = requests.get(url)
# 查看默认请求编码     ISO-8859-1
print(response.encoding)

# 设置响应编码
response.encoding = "utf-8"
# 查看响应内容 text形式
print(response.text)


'''
    encoding可以查看响应头部字符编码，也可设置
        eg： 默认百度的响应编码为 ISO-8859-1, text形式下，
                响应内容为： <title>ç¾åº¦ä¸ä¸ï¼ä½ å°±ç¥é</title>
        设置为“UTF-8”后
                响应内容为： <title>百度一下，你就知道</title>
'''
# 查看响应信息头   headers 信息比较重要，一般服务器返回的token/session相关信息都在headers中
print(response.headers)

# 获取响应cookies信息 返回字典对象
print(response.cookies)
print(response.cookies['BDORZ'])

url = "http://www.baidu.com/img/bd_logo1.png?where=super"
r = requests.get(url)
# 获取响应内容 字节形式
print(r.content)

# 将字节形式的响应内容，写入当前文件夹
with open("./baidu.png", "wb") as f:
    f.write(r.content)
