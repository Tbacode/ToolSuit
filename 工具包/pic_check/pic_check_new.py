'''
 * @Descripttion : 验证正式上线前，pic数据得一致性
 * @Author       : Tommy
 * @Date         : 2021-12-08 14:09:46
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-08 17:49:57
'''

from unittest.main import main
from typing import NoReturn
import requests
import time
import datetime
import json
from loguru import logger


class PicCheck():

    def __init__(self, url: str, game_ver: str, os_type: str) -> NoReturn:
        '''
         * @name: Tommy
         * @msg: 
         * @param {*} self
         * @param {str} url 请求地址
         * @param {str} game_ver 游戏版本号
         * @param {str} os_type 系统平台
         * @return {*}
        '''
        self.picname_list = []
        self.flag = 0
        self.keyword_list = [
            "picName", "picType", "picClass", "picUnlockDate",
            "picVipUnlockDate", "picExpireDate", "picUnlockType",
            "picUnlockNumber", "picJigsawId", "picOrder"
        ]
        self.pic_list_item = []
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.start_date = time.strftime("%Y%m%d", time.localtime())
        self.url = url
        self.params = {
            "game_ver": game_ver,
            "os_type": os_type,
            "register_ver": "7.4.0",
            "register_date": self.start_date,
            "game_date": self.game_date,
            "game_actDay": 1,
            "pic_type": "All",
            "start_date": self.start_date,
            "group_id": 20,
            "hide_finish": 0,
            "u_af_status": "Organic"
        }

    def new_api_params(self) -> NoReturn:
        '''
         * @name: Tommy
         * @msg: 修改新的接口使用参数
         * @param {*} self
         * @return {*}
        '''
        self.params['pic_type'] = 0
        self.params['resolu_width'] = 1080
        del self.params['u_af_status']

    def cmp_step_function(self, old_pic_check: 'PicCheck', new_pic_check: 'PicCheck') -> NoReturn:
        '''
         * @name: Tommy
         * @msg: 
         * @param {*} self
         * @param {*} old_pic_check 老接口PicCheck对象
         * @param {*} new_pic_check 新接口PicCheck对象
         * @return {*}
        '''
        print(11111)


if __name__ == "__main__":
    base_url = r'https://tapcolor-debug.taplayer.net/normalApi/v1/'
    old_url = ''.join([base_url, 'getGalleryList/'])
    new_url = ''.join([base_url, 'gallery/'])
    # old = PicCheck("url_old", "7.5.0","Android")
    print(old_url)
    print(new_url)
    p = PicCheck(old_url, "7.5.0", "Android")
    p.cmp_step_function(p, p)
    print(p.new_api_params.__doc__)
