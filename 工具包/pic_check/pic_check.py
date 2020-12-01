'''
 * @Descripttion : 验证正式上线前，pic数据得一致性
 * @Author       : Tommy
 * @Date         : 2020-11-05 15:24:58
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-01 14:35:52
'''

# TODO: 引包
import requests
import time
import datetime
import json
from loguru import logger


class PicCheck():
    def __init__(self, url: str, game_ver: str, os_type: str):
        '''
         * @name: Tommy
         * @msg: 类初始化参数构建
         * @param {*} self
         * @param {str} url
         * @param {str} game_ver
         * @param {str} os_type
         * @return {*}
        '''
        self.flag = 1
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
            "pic_type": "Jigsaw",
            "start_date": self.start_date,
            "group_id": 20
        }

    # TODO: 请求数据返回数据
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

    # TODO: 判断是否isEnd
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

    # TODO: 构造关键字提取数据
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
                dict_item[keyword_item] = pic_item[keyword_item]
            # dict_item = json.dumps(dict_item,
            #                        sort_keys=False,
            #                        indent=2,
            #                        ensure_ascii=False)
            self.pic_list_item.append(dict_item)
        logger.debug("构造数据结束")

    # TODO: 数据追加
    def add_pic_list(self, pic_list: list) -> list:
        '''
         * @name: Tommy
         * @msg: 数据追加
         * @param {*} self
         * @param {list} pic_list
         * @return {*}
        '''
        logger.debug("数据追加开始")
        return self.pic_list_item.append(pic_list)

    # TODO: 文件保存
    def save_json(self, flag: str):
        '''
         * @name: Tommy
         * @msg: 文件保存
         * @param {*} self
         * @param {str} flag ，标记new or old
         * @return {*}
        '''
        logger.debug("保存pic数据到json开始")
        with open("工具包/pic_check/" + flag + ".json", 'w+',
                  encoding='utf-8') as f:
            json.dump(self.pic_list_item, f, ensure_ascii=False, indent=2)
        logger.debug("保存pic数据到json结束")

    # TODO: 时间转换
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

    # TODO: pic_unlock时间节点提取，更换self.start_date
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

    # TODO: 主循环
    def main_function(self):
        '''
         * @name: Tommy
         * @msg: 主循环
         * @param {*} self
         * @return {*}
        '''
        if not self.isEnd_check():
            # TODO: 日期格式调整，使请求日期格式正确，功能正常
            self.time_change()
            logger.debug("此时的数据长度：" + str(len(self.pic_list_item)))
            logger.debug("开始新一轮递归")
            self.main_function()

    # TODO: json格式对比验证
    def json_file_check(self, old_json_item: dict, new_json_item: dict) -> bool:
        '''
         * @name: Tommy
         * @msg: json格式对比验证
         * @param {*} self
         * @param {dict} old_json_item
         * @param {dict} new_json_item
         * @return {bool}
        '''
        for keyword_item in self.keyword_list:
            if old_json_item[keyword_item] != new_json_item[keyword_item]:
                logger.debug("old_json于new_json中关键字：{}的值不相等。{} != {}".format(
                    keyword_item, old_json_item[keyword_item], new_json_item[keyword_item]))
                return False

    # TODO: 打开两个新旧json文件，并返回
    def open_json_file(self):
        '''
         * @name: Tommy
         * @msg: 打开两个新旧json文件，并返回
         * @param {*} self
         * @return {str} old_json, new_json
        '''
        logger.debug("打开相关json文件")
        with open("工具包/pic_check/old.json", "r", encoding="utf-8") as f:
            old_json = f.read()
        with open("工具包/pic_check/new.json", "r", encoding="utf-8") as a:
            new_json = a.read()
        return eval(old_json), eval(new_json)  # 风险转换 eval自动转换结构str->list[dict]

    # TODO: json格式校验
    def cmp(self, src_data, dst_data, con_key):
        '''
        @name: cmp
        @msg: 对比关键字并输出
        @param {验证数据，对比数据, 关键字}
        @return: none
        '''
        if isinstance(src_data, dict):
            for key in dst_data:
                if key not in src_data:
                    logger.error("旧文件不存在这个key：" + key)
            for key in src_data:
                if key in dst_data:
                    thiskey = key
                    self.cmp(src_data[thiskey], dst_data[thiskey], con_key)
                else:
                    logger.error("新文件不存在这个key：" + key)
        elif isinstance(src_data, list):

            if len(src_data) != len(dst_data):
                logger.error(
                    "list 长度：旧文件-{} != 新文件-{}".format(len(src_data), len(dst_data)))
            for src_list, dst_list in zip(
                    sorted(src_data, key=lambda x: x[con_key]),
                    sorted(dst_data, key=lambda x: x[con_key])):
                self.cmp(src_list, dst_list, con_key)
        else:
            if str(src_data) != str(dst_data):
                logger.error("存在不同值：{} 和 {}".format(src_data, dst_data))

    # TODO: jigsaw拼图检验
    def jigsaw_check(self):
        jigsaw_list = []
        flag = 1
        with open("工具包/pic_check/new.json", "r", encoding="utf-8") as a:
            new_json = a.read()
        new_json = eval(new_json)  # list强制转化
        for item in new_json:
            # logger.debug("开始遍历item == {}".format(item))
            if flag == 1:
                picJigsawId = item['picJigsawId']
                flag = 2
            if item['picClass'] == '':
                logger.error("图片{}存在picClass空值".format(item['picName']))
            if item['picJigsawId'] == picJigsawId:
                jigsaw_list.append(item['picName'])
            else:
                picJigsawId = item['picJigsawId']
                if len(jigsaw_list) % 2 == 0 and len(jigsaw_list) > 3:
                    logger.debug("当前jigsaw_list内容：{}".format(jigsaw_list))
                    jigsaw_list = []
                else:
                    logger.error("存在拼图数量不够的情况：{}".format(jigsaw_list))
                    jigsaw_list = []
                jigsaw_list.append(item["picName"])
        if len(jigsaw_list) != 0:
            if len(jigsaw_list) % 2 != 0 or len(jigsaw_list) < 4:
                logger.error("存在拼图数量不够的情况：{}".format(jigsaw_list))

                
# TODO: main
if __name__ == "__main__":
    now_time = datetime.datetime.now()
    logger.debug("程序开始时间：" + str(now_time))
    url = "https://tapcolor.weplayer.cc/"
    # url = "https://us-central1-tapcolor-new-debug.cloudfunctions.net/normalApi/"
    url = ''.join([url, 'normalApi/v1/getGalleryList'])
    game_ver = "4.7.0"
    os_type = "Android"
    pic_check = PicCheck(url, game_ver, os_type)
    pic_check.main_function()
    pic_check.save_json("new")
    end_time = datetime.datetime.now()
    ss = (end_time - now_time).seconds
    logger.debug("数据获取运行总时间：" + str(ss))
    pic_check.jigsaw_check()
    # old, new = pic_check.open_json_file()
    # pic_check.cmp(old, new, "picName")
