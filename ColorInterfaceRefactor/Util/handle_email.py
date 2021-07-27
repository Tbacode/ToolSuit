'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-07-26 17:04:50
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-07-26 17:07:46
'''
import requests


class HandleEmail(object):
    def __init__(self):
        self.id_url = r'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=eef716ba-a7e2-423e-9c9a-7cac807e397c&type=file'
        self.wx_url = r'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=eef716ba-a7e2-423e-9c9a-7cac807e397c'

    def post_file(self, file):
        data = {'file': open(file, 'rb')}
        # 请求id_url(将文件上传微信临时平台),返回media_id
        # id_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=xxx&type=file'
        response = requests.post(url=self.id_url, files=data)
        json_res = response.json()
        media_id = json_res['media_id']

        data = {"msgtype": "file", "file": {"media_id": media_id}}
        result = requests.post(url=self.wx_url, json=data)
        return (result)


handle_email = HandleEmail()