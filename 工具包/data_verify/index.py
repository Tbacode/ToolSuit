'''
 * @Descripttion : 脚本入口
 * @Author       : Tommy
 * @Date         : 2020-12-07 15:45:54
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-18 12:07:14
'''
from data_get import DataGet
from pic_verify import PicVerify
from loguru import logger
from info_robot import Robot
import json


def main(data_base: DataGet):
    # 主入口方法
    if not data_base.isEnd_check():
        data_base.time_change()
        logger.debug("此时的数据长度：" + str(len(data_base.pic_list_item)))
        logger.debug("开始新一轮递归")
        main(data_base)


def pre_main(url: str, game_ver: str, os_type: str, obj_name: str, env_name: str):
    # 这里验证数据的初始化
    pictype_list = [
        "Jigsaw", "Cartoon", "Fashion", "Food", "Marine", "Festival",
        "Unicorn", "Love", "Christmas", "Animated", "Special",
        "Character", "Animal", "Flower", "Place", "Nature",
        "Message", "Mosaic", "Mandala", "Other"
    ]
    for pic_type in pictype_list:
        logger.debug("请求开始类型：{}".format(pic_type))
        data_base = DataGet(url, game_ver, os_type, pic_type)
        pic_verify = PicVerify(obj_name, env_name)
        result = data_base.request_pic_list_item()
        # 第一层判断是否存在首次拉去就是空数据的分类
        if pic_verify.is_empty_by_pic_type(result['data']['picList']):
            # 非空就进入main函数递归获取整个分类下数据
            main(data_base)
            # 判断如果是拼图项目只需要验证Jigsaw分类
            if obj_name == "Jigsaw":
                logger.debug("这里是拼图分类，只做jigsaw分类验证，之后程序跳出")
                pic_verify.is_error_by_jigsawpic(data_base.pic_list_item)
                logger.debug("最后的数据：{}".format(
                    data_base.pic_list_item[-1]['picName']))
                break
            if pic_type == 'Jigsaw':
                pic_verify.is_error_by_jigsawpic(data_base.pic_list_item)
            logger.debug("最后的数据：{}".format(
                data_base.pic_list_item[-1]['picName']))
        else:
            msg_robot = Robot()
            # logger.error("存在分类{}数据为空".format(pic_type))
            content = "{}环境{}项目-存在{}分类数据为空".format(
                env_name, obj_name, pic_type)
            msg_robot.send_message(content)


def start(env_name: str, obj_name: str, os_type: str = "Android"):
    # 根据传入环境名称和项目名称来初始化参数
    with open("config.json", "r", encoding="utf-8") as f:
        con_json = f.read()
    con_json = json.loads(con_json)
    for key in con_json.keys():
        if key == env_name:
            # 匹配环境名以获取项目初始化参数
            for obj_item in con_json[key].keys():
                if obj_name == obj_item:
                    base_url = con_json[key][obj_item]['base_url']
                    api_name = con_json[key][obj_item]['Api_Name']
                    url = ''.join([base_url, api_name])
                    game_ver = con_json[key][obj_item]['game_ver']
                    os_type = os_type
                    logger.debug("项目参数初始化成功，进入main方法")
                    pre_main(url, game_ver, os_type, obj_name, env_name)
                    break


if __name__ == "__main__":
    start("pre", "TapColor")
