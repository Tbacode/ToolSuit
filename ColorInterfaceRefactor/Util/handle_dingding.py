'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-02-28 12:22:19
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-02-28 16:20:33
'''
from loguru import logger
import requests
import json


class HandleDing(object):

    def __init__(self, msg) -> None:
        self.msg = msg
        self.webhook = r"https://oapi.dingtalk.com/robot/send?access_token=9f3e0770e7429a1b72ec1337f7184b7935d378ecac3a8d1a808c9aa60cd197d4"

    def dingtalk(self, message):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'msgtype': 'markdown',
                'markdown': {
                    'title': self.msg,
                    'text': "### 填色接口报错信息\n\n"
                            "{}".format(message)
                }
                }
        r = requests.post(self.webhook, data=json.dumps(data), headers=headers)
        logger.debug("_"*20, r.text)
        return r.text


handle_ding = HandleDing("接口测试报错")
