'''
@Descripttion: 增加工具类，放入公用方法
@Author: Tommy
@Date: 2020-07-15 14:32:17
LastEditors: Tommy
LastEditTime: 2020-08-23 01:39:50
'''
import base64
from Crypto.Cipher import AES


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
                    Tool.cmp(src_data[thiskey], dst_data[thiskey], con_key)
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
                Tool.cmp(src_list, dst_list, con_key)
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
                        return False
        elif isinstance(data, dict):
            for key in data:
                if key in keylist:
                    continue
                else:
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
        for item in range(0, len(data)):
            if pic_Class not in data[item]['picClass']:
                return False
        return True

    def AES_Decrypt(aes_key, data):
        # data = data.encode('utf8')
        # 将加密数据转换位bytes类型数据
        encodebytes = base64.b64decode(data)
        vi = encodebytes[:16]
        test_encodebytes = encodebytes[16:]
        cipher = AES.new(aes_key.encode("utf-8"), AES.MODE_CBC, vi)

        text_decrypted = cipher.decrypt(test_encodebytes)
        # 去补位
        unpad = lambda s: s[0:-s[-1]]

        text_decrypted = unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted


if __name__ == '__main__':
    dict1 = {
        "picAssets": {
            "picNpic": {
                "md5":
                "ys87Fm2OoawCXrgH65BsWA==",
                "url":
                "lite/1.0/pics/pic_uLc4i7AfX/pic_uLc4i7AfX.npic?ver=ys87Fm2OoawCXrgH65BsWA=="
            },
            "picThumbnail": {
                "md5":
                "LnsHZH6hMDg34Tv6aUelTw==",
                "url":
                "lite/1.0/pics/pic_uLc4i7AfX/pic_uLc4i7AfX_thumbnail.png?ver=LnsHZH6hMDg34Tv6aUelTw=="
            },
            "picColorImg": {
                "md5":
                "9+jRyDsFqq4I5iK2JssKqQ==",
                "url":
                "lite/1.0/pics/pic_uLc4i7AfX/pic_uLc4i7AfX_color.png?ver=9+jRyDsFqq4I5iK2JssKqQ=="
            },
            "picFrameImg": {
                "md5":
                "iWCtztQC+KSxDvFaAlqM0A==",
                "url":
                "lite/1.0/pics/pic_uLc4i7AfX/pic_uLc4i7AfX_frame.png?ver=iWCtztQC+KSxDvFaAlqM0A=="
            }
        }
    }
    keylist = ["picNpic", "picThumbnail", "picColorImg", "picFrameImg"]
    Tool.check_isKeyword(dict1['picAssets'], keylist)
