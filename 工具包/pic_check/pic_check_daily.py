'''
 * @Descripttion : 验证正式上线前，pic数据得一致性
 * @Author       : Tommy
 * @Date         : 2021-12-08 14:09:46
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-04 16:55:51
'''
import time
import datetime
from typing import NoReturn
import requests
# import json
from loguru import logger


class PicCheck():

    def __init__(self, url: str, game_ver: str, os_type: str) -> NoReturn:
        '''
         * @name: Tommy
         * @msg: 类初始化参数构建
         * @param {*} self
         * @param {str} url 请求地址
         * @param {str} game_ver 游戏版本号
         * @param {str} os_type 系统平台
         * @return {*}
        '''
        self.picname_list = []
        self.flag = 0
        self.keyword_list = [
            "picName"
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
            "start_date": self.start_date,
            "end_date": "20181111",
            "group_id": 20,
            "u_af_status": "Organic"
        }

    def new_api_params(self) -> NoReturn:
        '''
         * @name: Tommy
         * @msg: 修改新的接口使用参数
         * @param {*} self
         * @return {*}
        '''
        self.params['resolu_width'] = 1079
        del self.params['u_af_status']

    def get_keyword_json(self, list_item: list) -> NoReturn:
        '''
         * @name: Tommy
         * @msg: 构造关键字提取数据
         * @param {*} self
         * @param {list} list_item 传入pic_list数组
         * @return {*}
        '''
        logger.debug("构造数据开始")
        for pic_item in list_item:
            dict_item = {}
            for keyword_item in self.keyword_list:
                if pic_item[keyword_item] != "":
                    dict_item[keyword_item] = pic_item[keyword_item]
            # dict_item = json.dumps(dict_item,
            #                        sort_keys=False,
            #                        indent=2,
            #                        ensure_ascii=False)
            self.pic_list_item.append(dict_item)
        logger.debug("构造数据结束")

    def update_start_date(self, pic_list: list) -> NoReturn:
        '''
         * @name: Tommy
         * @msg: 更新start_date以获取下个时间节点的图片数据
         * @param {*} self
         * @param {list} pic_list 图片数据集合
         * @return {*}
        '''
        self.params['start_date'] = pic_list[-1]['picUnlockDate']
        logger.debug("数据返回更新后得时间:" + str(self.params['start_date']))

    def time_change(self) -> NoReturn:
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
        logger.debug("日期减一:" + str(self.params['start_date']))

    def request_pic_list_item(self, method: str = 'get') -> dict:
        '''
         * @name: Tommy
         * @msg: 请求数据返回数据
         * @param {*} self
         * @return {*} 返回当前请求结果
        '''
        if method.lower() == 'get':
            logger.debug("GET请求开始，请求日期:" + str(self.params['start_date']))
            pic_item = requests.get(self.url, params=self.params)
            logger.debug("请求url完整路径:" + str(pic_item.url))
        else:
            logger.debug("POST请求开始，请求日期:" + str(self.params['start_date']))
            pic_item = requests.post(self.url, data=self.params)
            logger.debug("请求url完整路径:" + str(pic_item.url))
        result = pic_item.json()
        return result

    def is_end_check(self, method: str = 'get') -> bool:
        '''
         * @name: Tommy
         * @msg: 判断接口数据是否结束
         * @param {*} self
         * @return {*} 真假
        '''
        logger.debug("判断是否结束")
        result = self.request_pic_list_item(method)
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

    def cmp_conkey(self, src_data: list, dst_data: list, con_key: str) -> NoReturn:
        '''
         @name: cmp
         @msg: 对比关键字并输出
         @param {验证数据，对比数据, 关键字}
         @return: 
        '''
        if isinstance(src_data, dict):
            self.cmp_conkey(src_data[con_key], dst_data[con_key], con_key)
        elif isinstance(src_data, list):

            if len(src_data) != len(dst_data):
                logger.error("list 长度: 旧文件-{} != 新文件-{}".format(
                    len(src_data), len(dst_data)))
            src_data = sorted(src_data, key=lambda x: x[con_key])
            dst_data = sorted(dst_data, key=lambda x: x[con_key])
            for index in range(len(dst_data)):
                self.cmp_conkey(
                    src_data[index - self.flag], dst_data[index], con_key)
        else:
            if str(src_data) != str(dst_data):
                logger.error("存在不同值: {} 和 {}".format(src_data, dst_data))
                self.flag += 1
                self.picname_list.append(dst_data)
                return False

    def cmp_step_function(self, old_pic_check: 'PicCheck', new_pic_check: 'PicCheck') -> NoReturn:
        '''
         * @name: Tommy
         * @msg: 对比数据方法
         * @param {*} self
         * @param {*} old_pic_check 老接口PicCheck对象
         * @param {*} new_pic_check 新接口PicCheck对象
         * @return {*}
        '''
        if not old_pic_check.is_end_check():
            old_pic_item = old_pic_check.pic_list_item
            logger.info("老接口数据长度:" + str(len(old_pic_item)))
            old_pic_item = sorted(old_pic_item, key=lambda x: x["picName"])
            # old_pic_check.save_json("old_nUser" + str(self.flag))

        if not new_pic_check.is_end_check('post'):
            new_pic_item = new_pic_check.pic_list_item
            logger.error("新接口数据长度:" + str(len(new_pic_item)))
            new_pic_item = sorted(new_pic_item, key=lambda x: x["picName"])
            # new_pic_check.save_json("new_nUser" + str(self.flag))

            new_pic_check.cmp_conkey(old_pic_item, new_pic_item, "picName")
            # old_pic_check.time_change()
            # new_pic_check.time_change()
            # self.flag += 1
            # self.cmp_step_function(old_pic_check, new_pic_check)


if __name__ == "__main__":
    base_url = r'https://tapcolor.taplayer.net/normalApi/v1/'
    url = r'https://tapcolor.taplayer.net/normalApi/v1/'
    old_url = ''.join([url, 'getDailyList/'])
    new_url = ''.join([base_url, 'daily/'])
    p1 = PicCheck(old_url, "7.5.0", "Android")
    p2 = PicCheck(new_url, "7.5.0", "Android")
    p2.new_api_params()
    p1.cmp_step_function(p1, p2)
