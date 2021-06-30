'''
@Descripttion: 增加工具类，放入公用方法
@Author: Tommy
@Date: 2020-07-15 14:32:17
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-17 11:05:57
'''
import json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import base64
# from Crypto.Cipher import AES


class Tool(object):
    flag = 1

    def cmp(src_data, dst_data, con_key):
        '''
        @name: cmp
        @msg: 对比关键字并输出
        @param {验证数据， 对比数据, 关键字}
        @return: none
        '''
        if isinstance(src_data, dict):
            for key in dst_data:
                if key not in src_data:
                    print("  " * Tool.flag + "Key:" + str(key))
                    print("  " * Tool.flag + "新接口不存在这个key: " + key)
            for key in src_data:
                print("  " * Tool.flag + "Key:" + str(key))
                if key in dst_data:
                    thiskey = key
                    Tool.flag += 1
                    self.cmp(src_data[thiskey], dst_data[thiskey], con_key)
                else:
                    print("  " * Tool.flag + "旧接口不存在这个key: " + key)
            Tool.flag -= 1
        elif isinstance(src_data, list):

            if len(src_data) != len(dst_data):
                print("list 长度: '{}' != '{}'".format(len(src_data),
                                                     len(dst_data)))
            for src_list, dst_list in zip(
                    sorted(src_data, key=lambda x: x[con_key]),
                    sorted(dst_data, key=lambda x: x[con_key])):
                Tool.flag += 1
                self.cmp(src_list, dst_list, con_key)
            Tool.flag -= 1
        else:
            Tool.flag -= 1
            if str(src_data) != str(dst_data):
                print("  " * Tool.flag +
                      "存在不同值: {} 和 {}".format(src_data, dst_data))

    def check_type(data: list, Type: str) -> bool:
        '''
        @name: check_type
        @msg: 检查数据格式
        @param {待测数据, 对比类型}
        @return: bool
        '''
        for item in data:
            if isinstance(item, Type):
                continue
            else:
                return False
        return True

    def check_isKeyword(data, keylist: list) -> bool:
        '''
        @name: check_isKeyword
        @msg: 检查待测数据是否含有验证关键字
        @param {待测数据, 验证关键字集合}
        @return: bool
        '''
        if isinstance(data, list):
            for item in data:
                for key in item:
                    if key in keylist:
                        continue
                    else:
                        print(key)
                        return False
        elif isinstance(data, dict):
            for key in data:
                if key in keylist:
                    continue
                else:
                    print(key)
                    return False
        return True

    def check_isKeyword_picAssets(data: list, keylist: list) -> bool:
        '''
        @name: check_isKeyword_picAssets
        @msg: 对传入得每一个picAssets数据验证是否含有验证关键字
        @param {待测数据, 验证关键字集合}
        @return: bool
        '''
        ap_keylist = keylist
        ap_keylist.append("picFaLine")
        ap_keylist.append("picFaColor")
        ap_keylist.append("picAb")
        for item in range(0, len(data)):
            if "ap_" not in data[item]['picName']:
                for key in data[item]['picAssets']:
                    if key in keylist:
                        continue
                    else:
                        return False
            else:
                for key in data[item]['picAssets']:
                    if key in ap_keylist:
                        continue
                    else:
                        return False
        return True

    def check_pic_type(data: list, pic_Class: str) -> bool:
        '''
        @name: check_pic_type
        @msg: 验证传入得图片数据,是否类型正确
        @param {待测数据, 验证类型关键字}
        @return: bool
        '''
        if len(data) == 0:
            return False
        else:
            for item in range(0, len(data)):
                if pic_Class not in data[item]['picClass']:
                    return False
            return True

    # async def get_media_id(report_dir):
    #    report_dir = './reports/2020-08-11 15_54_13 test_report.txt'
    #    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=5aae35f3-110c-4729-b776-8ad6413127db&type=file'
    #    media_id = ""
    #    async with aiohttp.ClientSession() as session:
    #        data = aiohttp.FormData()
    #        data.add_field('file_1', open(report_dir, 'rb'), filename='testReport.txt',content_type='multipart/form-data')
    #        async with session.post(url, data=data) as resp:
    #            print(await resp.text())
    #            mytext = asyncio.run(self.send_request())
    #            media_id = json.loads(mytext)['media_id']
    #            return media_id

    # async def send_request():
    #    async with aiohttp.ClientSession() as session:
    #        data = aiohttp.FormData()
    #        data.add_field('file_1', open(report_dir, 'rb'), filename='testReport.txt',
    #                       content_type='multipart/form-data')
    #        async with session.post(url, data=data) as resp:
    #            print(await resp.text())
    #            return await resp.text()

    # 企业微信发送
    def call_wechat_media(url, media_id):
        data_report = {"msgtype": "file", "file": {"media_id": media_id}}
        data_json = json.dumps(data_report)  # dumps：将python对象解码为json数据
        requests.post(url, data_json)

    def call_wechat_txt(self, url, txt_data):
        data_report = {"msgtype": "text", "text": {"content": txt_data}}
        data_json = json.dumps(data_report)  # dumps：将python对象解码为json数据
        requests.post(url, data_json)

    # 邮件发送
    def send_mail(file_new, receiver_list):
        user = '875932826'
        pwd = 'hbuoqldeufbxbbhj'
        sender = '875932826@qq.com'
        receiver_list = ['xt875932826@126.com']
        '''定义发送邮件'''
        f = open(file_new, 'rb')
        mail_body = f.read()
        f.close()
        sendfile = open(file_new, 'rb').read()

        att = MIMEText(sendfile, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="report.html"'

        msgRoot = MIMEMultipart()
        msgRoot.attach(MIMEText(mail_body, 'html', 'utf-8'))
        msgRoot['Subject'] = Header("自动化测试报告", 'utf-8')
        msgRoot.attach(att)

        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtp.login(user, pwd)
        for x in receiver_list:
            smtp.sendmail(sender, x, msgRoot.as_string())
        print('email has send out')

    def get_event_id(url: str) -> dict:
        r = requests.get(url=url)
        result = r.json()
        return result

    def AES_Decrypt(key, data):
        data = data.encode('utf8')
        # 将加密数据转换位bytes类型数据
        encodebytes = base64.b64decode(data)
        vi = encodebytes[:16]
        test_encodebytes = encodebytes[16:]
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi)

        text_decrypted = cipher.decrypt(test_encodebytes)
        # 去补位
        def unpad(s): return s[0:-s[-1]]

        text_decrypted = unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    def request_get_result(url, parm) -> dict:
        r = requests.get(url, params=parm)
        # aes_result = Tool.AES_Decrypt("talefuntapcolor!", r.text)
        # result = json.loads(aes_result)
        result = r.json()
        print(result)
        return result

    def request_post_result(url, data) -> dict:
        r = requests.post(url, data=data)
        # aes_result = Tool.AES_Decrypt("talefuntapcolor!", r.text)
        # result = json.loads(aes_result)
        result = r.json()
        return result


if __name__ == '__main__':
    pass
