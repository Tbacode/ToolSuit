'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-07-26 17:04:50
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-06 16:09:50
'''
import requests


class HandleEmail(object):
    def __init__(self):
        self.id_url = r'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=834bddac-9977-4cf4-a517-dc4a9a736d6f&type=file'
        self.wx_url = r'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=834bddac-9977-4cf4-a517-dc4a9a736d6f'
        self.id_url_qa = r'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=708fa9fb-47e8-4db2-b0b2-dd9abd1d532d&type=file'
        self.wx_url_qa = r'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=708fa9fb-47e8-4db2-b0b2-dd9abd1d532d'
        # https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=834bddac-9977-4cf4-a517-dc4a9a736d6f

    def post_file(self, file, qa):
        if qa:
            id_url = self.id_url_qa
            wx_url = self.wx_url_qa
        # else:
        #     id_url = self.id_url
        #     wx_url = self.wx_url
        data = {'file': open(file, 'rb')}
        # 请求id_url(将文件上传微信临时平台),返回media_id
        # id_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=xxx&type=file'
        response = requests.post(url=id_url, files=data)
        json_res = response.json()
        media_id = json_res['media_id']

        data = {"msgtype": "file", "file": {"media_id": media_id}}
        result = requests.post(url=wx_url, json=data)
        return (result)


handle_email = HandleEmail()
