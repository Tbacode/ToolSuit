'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-12-15 16:42:31
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-15 18:21:50
'''
from logging import log
import time
import requests
from loguru import logger


class PicCheck():

    def __init__(self, url: str, game_ver: str, os_type: str) -> None:
        '''
         * @name: Tommy
         * @msg: 
         * @param {*} self
         * @param {str} url
         * @param {str} game_ver
         * @param {str} os_type
         * @return {*}
        '''
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.start_date = time.strftime("%Y%m%d", time.localtime())
        self.params = {
            "game_ver": game_ver,
            "os_type": os_type,
            "register_ver": "7.4.0",
            "register_date": self.start_date,
            "game_date": self.game_date,
            "game_actDay": 1,
            "start_date": self.start_date,
            "group_id": 20,
            "hide_finish": 0,
            "resolu_width": 1079
        }
        self.url = url

    def get_Galleries_Data(self) -> dict:
        '''
         * @name: Tommy
         * @msg: 获取接口数据
         * @param {*} self
         * @return {dict} 返回数据
        '''
        logger.debug("请求开始, 请求日期: " + self.params['game_date'])
        res = requests.post(url=self.url, data=self.params).json()
        return res

    def picClass_Check(self, pic_info_list: list, pic_class: str) -> None:
        '''
         * @name: Tommy
         * @msg: 分类一致性检测实现
         * @param {*} self
         * @param {list} pic_info_list
         * @param {str} pic_class
         * @return {*}
        '''
        for pic_info_itme in pic_info_list:
            if pic_class not in pic_info_itme['picClass']:
                logger.error("{}存在picClass与分类不符: {} is not in {}".format(
                    pic_info_itme['picName'], pic_class, pic_info_itme['picClass']))
            else:
                logger.debug("{}存在picClass与分类一致: {} is in {}".format(
                    pic_info_itme['picName'], pic_class, pic_info_itme['picClass']))

    def allClassPicinfo_Check(self) -> None:
        '''
         * @name: Tommy
         * @msg: galleries 分类一致性检测主方法
         * @param {*} self
         * @return {*}
        '''
        res = self.get_Galleries_Data()['data']['allClassPicInfo']
        for item in res:
            if item['picClass'] == "0":
                logger.debug("ALL分类请求，不做分类一致性测试")
            else:
                picClass = item['picClass']
                pic_info_list = item['picList']
                logger.debug("开始picClass一致性测试")
                self.picClass_Check(pic_info_list, picClass)

    def get_PicClass_Key(self, res):
        picClass_key = {}
        # res = self.get_Galleries_Data()['data']['config']['classic']['tagid']
        tagid_list = res.split("|")
        for tag_item in tagid_list:
            picClass_key[tag_item.split(",")[1]] = tag_item.split(",")[0]
        return picClass_key

    def get_Oldpicinfo(self, pic_type: str) -> dict:
        url = r'https://tapcolor.taplayer.net/normalApi/v1/getGalleryList/'
        self.params['pic_type'] = pic_type
        self.params['u_af_status'] = "Organic"
        del self.params['resolu_width']
        res = requests.get(url=url, params=self.params).json()

    def allPicname_Check(self) -> None:
        new_picinfo_dict = self.get_Galleries_Data()

        picClass_key_dict = self.get_PicClass_Key(new_picinfo_dict['data']['config']['classic']['tagid'])
        print(picClass_key_dict)



if __name__ == "__main__":
    base_url = r'https://tapcolor-new-pre.taplayer.net/normalApi/v1/galleries/'
    p = PicCheck(base_url, "7.5.0", "Android")
    # p.allClassPicinfo_Check()
    p.allPicname_Check()
