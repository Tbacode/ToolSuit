'''
 * @Descripttion : 消息提醒机器人
 * @Author       : Tommy
 * @Date         : 2020-12-14 14:30:56
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-15 20:57:21
'''
import requests
from loguru import logger


class Robot(object):
    def __init__(self):
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=693f02e4-5c06-4ff4-88a3-fe6e1295994c"
        self.headers = {"Content-Type": "text/json"}
        self.data = {}

    def send_message(self, content):
        self.data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        logger.error("错误信息：{}".format(content))
        # requests.post(url=self.url, headers=self.headers, json=self.data)
