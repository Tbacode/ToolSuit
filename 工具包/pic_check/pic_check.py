'''
 * @Descripttion: 验证正式上线前，pic数据得一致性
 * @Author: Tommy
 * @Date: 2020-11-05 15:24:58
 * @LastEditors: Tommy
 * @LastEditTime: 2020-11-10 17:36:18
'''

# TODO: 引包
import requests
import time
import datetime
import json
from loguru import logger


class PicCheck():
    '''
     * @name: Tommy
     * @msg: 类初始化参数构建
     * @param {*} self
     * @param {str} url
     * @param {str} game_ver
     * @param {str} os_type
     * @return {*}
    '''
    def __init__(self, url: str, game_ver: str, os_type: str):
        self.pic_list_item = []
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.start_date = time.strftime("%Y%m%d", time.localtime())
        self.url = url
        self.params = {
            "game_ver": game_ver,
            "os_type": os_type,
            "register_date": self.start_date,
            "game_date": self.game_date,
            "game_actDay": 1,
            "pic_type": "All",
            "start_date": self.start_date,
            "group_id": 20
        }

    # TODO: 请求数据返回数据
    '''
     * @name: Tommy
     * @msg: 请求数据返回数据
     * @param {*} self
     * @return {*}
    '''

    def request_pic_list_item(self) -> dict:
        logger.debug("请求开始，请求日期：" + str(self.params['start_date']))
        pic_item = requests.get(self.url, params=self.params)
        # pic_item = json.dumps(pic_item.json(),
        #                       indent=2,
        #                       sort_keys=False,
        #                       ensure_ascii=False)
        pic_item = pic_item.json()
        return pic_item

    # TODO: 判断是否isEnd
    '''
     * @name: Tommy
     * @msg: 判断是否isEnd
     * @param {*} self
     * @return {*}
    '''

    def isEnd_check(self):
        logger.debug("判断是否结束")
        result = self.request_pic_list_item()
        if bool(result['data']['isEnd']):
            logger.debug("数据结束，返回True")
            return True
        else:
            logger.debug("数据未结束，返回False")
            self.update_start_date(result['data']['picList'])
            self.get_keyword_json(result['data']['picList'])
            return False

    # TODO: 构造关键字提取数据
    '''
     * @name: Tommy
     * @msg: 构造关键字提取数据
     * @param {*} self
     * @param {list} list_item
     * @return {*}
    '''

    def get_keyword_json(self, list_item: list) -> dict:
        logger.debug("构造数据开始")
        for pic_item in list_item:
            dict_item = {}
            dict_item['picName'] = pic_item['picName']
            dict_item['picType'] = pic_item['picType']
            dict_item['picClass'] = pic_item['picClass']
            dict_item['picUnlockDate'] = pic_item['picUnlockDate']
            dict_item['picVipUnlockDate'] = pic_item['picVipUnlockDate']
            dict_item['picExpireDate'] = pic_item['picExpireDate']
            dict_item['picUnlockType'] = pic_item['picUnlockType']
            dict_item['picUnlockNumber'] = pic_item['picUnlockNumber']
            dict_item['picJigsawId'] = pic_item['picJigsawId']
            dict_item['picOrder'] = pic_item['picOrder']
            dict_item['picComicId'] = pic_item['picComicId']
            dict_item['picComicKey'] = pic_item['picComicKey']
            dict_item = json.dumps(dict_item,
                                   sort_keys=False,
                                   indent=2,
                                   ensure_ascii=False)
            self.pic_list_item.append(dict_item)
        logger.debug("构造数据结束")

    # TODO: 数据追加
    '''
     * @name: Tommy
     * @msg: 数据追加
     * @param {*} self
     * @param {list} pic_list
     * @return {*}
    '''

    def add_pic_list(self, pic_list: list) -> list:
        logger.debug("数据追加开始")
        return self.pic_list_item.append(pic_list)

    # TODO: 文件保存
    '''
     * @name: Tommy
     * @msg: 文件保存
     * @param {*} self
     * @return {*}
    '''

    def save_json(self):
        pass

    # TODO: 时间转换
    '''
     * @name: Tommy
     * @msg: 时间转换
     * @param {*} self
     * @return {*}
    '''

    def time_change(self):
        timeArray = time.strptime(str(self.params['start_date']), "%Y%m%d")
        now = int(time.mktime(timeArray))
        now = datetime.datetime.fromtimestamp(now)
        delta = datetime.timedelta(days=1)
        n_days = now - delta
        self.params['start_date'] = n_days.strftime('%Y%m%d')
        logger.debug("日期减一：" + str(self.params['start_date']))

    # TODO: pic_unlock时间节点提取，更换self.start_date
    '''
     * @name: Tommy
     * @msg: 更新start_date
     * @param {*} self
     * @param {list} pic_list
     * @return {*}
    '''

    def update_start_date(self, pic_list: list):
        self.params['start_date'] = pic_list[-1]['picUnlockDate']
        logger.debug("数据返回更新后得时间：" + str(self.params['start_date']))

    # TODO: 主循环
    '''
     * @name: Tommy
     * @msg: 主循环
     * @param {*} self
     * @return {*}
    '''

    def main_function(self):
        if not self.isEnd_check():
            # TODO: 日期格式调整，使请求日期格式正确，功能正常
            self.time_change()
            logger.debug("此时的数据长度：" + str(len(self.pic_list_item)))
            logger.debug("开始新一轮递归")
            self.main_function()


# TODO: main
if __name__ == "__main__":
    now_time = datetime.datetime.now()
    logger.debug("程序开始时间：" + str(now_time))
    url = "https://us-central1-tapcolor-new-debug.cloudfunctions.net/normalApi/"
    url = ''.join([url, 'normalApi/v1/getGalleryList'])
    game_ver = "4.7.0"
    os_type = "Android"
    pic_check = PicCheck(url, game_ver, os_type)
    pic_check.main_function()
    end_time = datetime.datetime.now()
    ss = (end_time - now_time).seconds
    logger.debug("程序运行总时间：" + str(ss))
    # print(pic_check.pic_list_item)
