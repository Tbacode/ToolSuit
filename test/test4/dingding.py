'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-02-08 19:00:48
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-02-08 19:00:48
'''

import requests
import json


def getAccess_token():
    appkey = '****'  
    appsecret = '****' 

    url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (appkey, appsecret)

    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }
    data = {'appkey': appkey,
            'appsecret': appsecret}
    r = requests.request('GET', url, data=data, headers=headers)
    access_token = r.json()["access_token"]
    return access_token


def getMedia_id():
    access_token = getAccess_token()  # 拿到接口凭证
    path = './helloworld.txt'  # 文件地址
    url = 'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
    files = {'media': open(path, 'rb')}
    data = {'access_token': access_token,
            'type': 'file'}
    response = requests.post(url, files=files, data=data)
    json = response.json()
    return json["media_id"]


def SendFile():
    access_token = getAccess_token()
    media_id = getMedia_id()
    chatid = '****'  # 通过jsapi工具获取的群聊id
    url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
    header = {
        'Content-Type': 'application/json'
    }
    data = {'access_token': access_token,
            'chatid': chatid,
            'msg': {
                'msgtype': 'file',
                'file': {'media_id': media_id}
            }}
    r = requests.request('POST', url, data=json.dumps(data), headers=header)
    print(r.json())


SendFile()


