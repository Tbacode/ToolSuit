'''
 * @Descripttion : 脚本入口
 * @Author       : Tommy
 * @Date         : 2020-12-07 15:45:54
 * @LastEditors  : Tommy
 * @LastEditTime : 2020-12-08 16:32:53
'''
from data_get import DataGet
from pic_verify import PicVerify
from loguru import logger


def main(data_base: DataGet):
    # 主入口方法
    if not data_base.isEnd_check():
        data_base.time_change()
        logger.debug("此时的数据长度：" + str(len(data_base.pic_list_item)))
        logger.debug("开始新一轮递归")
        main(data_base)


if __name__ == "__main__":
    base_url = "https://tapcolor.weplayer.cc/"
    url = ''.join([base_url, 'normalApi/v1/getGalleryList'])
    game_ver = "4.7.0"
    os_type = "Android"
    pictype_list = [
        "Jigsaw", "Cartoon", "Fashion", "Food", "Marine", "Festival",
        "Unicorn", "Love", "Christmas", "Animated", "Special",
        "Character", "Animal", "Flower", "Place", "Nature",
        "Message", "Mosaic", "Mandala", "Other"
    ]
    for pic_type in pictype_list:
        logger.debug("请求开始类型：{}".format(pic_type))
        data_base = DataGet(url, game_ver, os_type, pic_type)
        pic_verify = PicVerify()
        result = data_base.request_pic_list_item()
        if pic_verify.is_empty_by_pic_type(result['data']['picList']):
            main(data_base)
            if pic_type == 'Jigsaw':
                pic_verify.is_error_by_jigsawpic(data_base.pic_list_item)
            logger.debug("最后的数据：{}".format(data_base.pic_list_item[-1]['picName']))
        else:
            logger.error("存在分类{}数据为空".format(pic_type))
