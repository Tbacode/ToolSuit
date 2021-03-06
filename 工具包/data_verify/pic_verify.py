'''
 * @Descripttion : 数据处理类
 * @Author       : Tommy
 * @Date         : 2020-12-07 11:50:13
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-16 14:22:09
'''
from loguru import logger
from info_robot import Robot


class PicVerify(object):
    def __init__(self, project_name, env_name):
        self.env_name = env_name
        self.project_name = project_name
        self.msg_robot = Robot()

    # TODO: 判断分类是否为空数据
    def is_empty_by_pic_type(self, pic_list: list):
        '''
         * @name: Tommy
         * @msg: 判断分类是否为空数据
         * @param {*} self
         * @param {list} pic_list
         * @return {*}
        '''
        if len(pic_list) == 0:
            return False
        else:
            return True

    # TODO: 判断分类数据内是否分类正确
    def is_type_error_by_pic_type(self, pic_type: str, pic_list: list):
        '''
         * @name: Tommy
         * @msg: 判断分类数据内是否分类正确
         * @param {*} self
         * @param {str} pic_type
         * @param {list} pic_list
         * @return {*}
        '''
        for item in pic_list:
            if pic_type not in item['picClass']:
                # logger.error("图片:{}不是{}分类".format(
                #     item['picName'], item['picClass']))
                content = "{}环境{}项目-图片:{}不是{}分类".format(
                    self.env_name, self.project_name, item['picName'], item['picClass'])
                self.msg_robot.send_message(content)

    # TODO: 判断拼图数据是否异常
    def is_error_by_jigsawpic(self, pic_list_jigsaw: list):
        '''
         * @name: Tommy
         * @msg: 判断拼图数据是否异常
         * @param {*} self
         * @return {*}
        '''
        jigsaw_list = []
        flag = 1
        # new_json = []
        # TODO: 这里需要加入拼图数据传入
        # with open("工具包/pic_check/new.json", "r", encoding="utf-8") as a:
        #     new_json = a.read()
        # new_json = eval(new_json)  # list强制转化
        for item in pic_list_jigsaw:
            # logger.debug("开始遍历item == {}".format(item))
            if flag == 1:
                picJigsawId = item['picJigsawId']
                flag = 2
            if item['picClass'] == '':
                # logger.error("图片{}存在picClass空值".format(item['picName']))
                content = "{}环境{}项目-图片{}存在picClass空值".format(
                    self.env_name, self.project_name, item['picName'])
                self.msg_robot.send_message(content)
            if item['picJigsawId'] == picJigsawId:
                jigsaw_list.append(item['picName'])
            else:
                picJigsawId = item['picJigsawId']
                if len(jigsaw_list) % 2 == 0 and len(jigsaw_list) > 3:
                    logger.debug("当前jigsaw_list内容：{}".format(jigsaw_list))
                    jigsaw_list = []
                else:
                    # logger.error("存在拼图数量不够的情况：{}".format(jigsaw_list))
                    content = "{}环境{}项目-存在拼图数量小于4的情况：{}".format(
                        self.env_name, self.project_name, jigsaw_list)
                    self.msg_robot.send_message(content)
                    jigsaw_list = []
                jigsaw_list.append(item["picName"])
        if len(jigsaw_list) != 0:
            if len(jigsaw_list) % 2 != 0 or len(jigsaw_list) < 4:
                # logger.error("存在拼图数量不够的情况：{}".format(jigsaw_list))
                content = "{}环境{}项目-存在拼图数量小于4的情况：{}".format(
                    self.env_name, self.project_name, jigsaw_list)
                self.msg_robot.send_message(content)
