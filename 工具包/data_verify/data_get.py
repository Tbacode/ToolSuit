'''
 * @Descripttion : 数据获取类
 * @Author       : Tommy
 * @Date         : 2020-12-07 11:23:24
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-14 15:24:12
'''
import requests
import time
from loguru import logger
import datetime


class DataGet(object):

    def __init__(self, url: str, game_ver: str, os_type: str, pic_type: str):
        '''
         * @name: Tommy
         * @msg: 构造方法
         * @param {*} self
         * @param {str} url
         * @param {str} game_ver
         * @param {str} os_type
         * @return {*}
        '''
        self.keyword_list = ["picName",
                             "picType",
                             "picClass",
                             "picUnlockDate",
                             "picVipUnlockDate",
                             "picExpireDate",
                             "picUnlockType",
                             "picUnlockNumber",
                             "picJigsawId",
                             "picOrder",
                             "picComicId",
                             "picComicKey"
                             ]
        self.game_date = time.strftime("%Y%m%d", time.localtime())
        self.start_date = time.strftime("%Y%m%d", time.localtime())
        self.url = url
        self.pic_list_item = []
        self.params = {
            "game_ver": game_ver,
            "os_type": os_type,
            "register_date": self.start_date,
            "game_date": self.game_date,
            "game_actDay": 1,
            "pic_type": pic_type,
            "start_date": self.start_date,
            "group_id": 20
        }

    def request_pic_list_item(self) -> dict:
        '''
         * @name: Tommy
         * @msg: 请求数据返回数据
         * @param {*} self
         * @return {*}
        '''
        logger.debug("请求开始，请求日期：" + str(self.params['start_date']))
        pic_item = requests.get(self.url, params=self.params)
        # pic_item = json.dumps(pic_item.json(),
        #                       indent=2,
        #                       sort_keys=False,
        #                       ensure_ascii=False)
        result = pic_item.json()
        return result

    def isEnd_check(self):
        '''
         * @name: Tommy
         * @msg: 判断是否isEnd
         * @param {*} self
         * @return {*}
        '''
        logger.debug("判断是否结束")
        result = self.request_pic_list_item()
        if bool(result['data']['isEnd']):
            logger.debug("数据结束，返回True")
            if len(result['data']['picList']) != 0:
                self.get_keyword_json(result['data']['picList'])
            return True
        else:
            logger.debug("数据未结束，返回False")
            self.update_start_date(result['data']['picList'])
            self.get_keyword_json(result['data']['picList'])
            return False

    def time_change(self):
        '''
         * @name: Tommy
         * @msg: 时间转换，减一天更新新的请求start_date
         * @param {*} self
         * @return {*}
        '''
        timeArray = time.strptime(str(self.params['start_date']), "%Y%m%d")
        now = int(time.mktime(timeArray))
        now = datetime.datetime.fromtimestamp(now)
        delta = datetime.timedelta(days=1)
        n_days = now - delta
        self.params['start_date'] = n_days.strftime('%Y%m%d')
        logger.debug("日期减一：" + str(self.params['start_date']))

    def update_start_date(self, pic_list: list):
        '''
         * @name: Tommy
         * @msg: 更新start_date
         * @param {*} self
         * @param {*} pic_list
         * @return {*}
        '''
        self.params['start_date'] = pic_list[-1]['picUnlockDate']
        logger.debug("数据返回更新后得时间：" + str(self.params['start_date']))

    def get_keyword_json(self, list_item: list) -> dict:
        '''
         * @name: Tommy
         * @msg: 构造关键字提取数据
         * @param {*} self
         * @param {list} list_item
         * @return {*}
        '''
        logger.debug("构造数据开始")
        for pic_item in list_item:
            dict_item = {}
            for keyword_item in self.keyword_list:
                try:
                    dict_item[keyword_item] = pic_item[keyword_item]
                except KeyError:
                    continue
                # dict_item[keyword_item] = pic_item[keyword_item]
            # dict_item = json.dumps(dict_item,
            #                        sort_keys=False,
            #                        indent=2,
            #                        ensure_ascii=False)
            self.pic_list_item.append(dict_item)
        logger.debug("构造数据结束")
