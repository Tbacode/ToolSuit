'''
Description: 
Autor: Tommy
Date: 2020-08-15 15:52:56
LastEditors: Tommy
LastEditTime: 2020-08-15 16:24:05
'''
from Crypto.Cipher import AES
import base64


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def AES_Encrypt(self, data):
        vi = '0102030405060708'
        # 字符串补位
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(data)

        # 加密后得到的是bytes类型的数据
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC,
                         vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        encryptedbytes = vi.encode('utf8') + encryptedbytes
        # 使用Base64进行编码,返回byte字符串
        encodestrs = base64.b64encode(encryptedbytes)
        # 对byte字符串按utf-8进行解码
        enctext = encodestrs.decode('utf8')
        return enctext

    def AES_Decrypt(self, data):
        data = data.encode('utf8')
        # 将加密数据转换位bytes类型数据
        encodebytes = base64.b64decode(data)
        vi = encodebytes[:16]
        test_encodebytes = encodebytes[16:]
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, vi)

        text_decrypted = cipher.decrypt(test_encodebytes)
        # 去补位
        unpad = lambda s: s[0:-s[-1]]

        text_decrypted = unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted


if __name__ == '__main__':
    pc = prpcrypt('talefuntapcolor!')  # 初始化密钥
    e = pc.AES_Encrypt('"helloworld"')
    print(e)
    d = pc.AES_Decrypt("Y0cnWBoiCut94AMUSl3pMvnRthel8jT0X/5A8CiEZJM=")
    print(d)
