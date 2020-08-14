# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-07-05 10:32:37
# @Last Modified by:   Tommy
# @Last Modified time: 2019-07-24 12:19:13
import os
import difflib
import shutil
import traceback
import logging
import pyprind
from table_operation import Table_Operation
from api_operation import Api_operation


platform_dict = {
    "1": "ios",
    "2": "android"
}

packname_dict = {
    "1": "com.pixel.art.coloring.by.number",
    "2": "com.relax.coloring.games.color.by.number.colourpop",
    "3": "com.coloring.games.doodle.paint.number",
    "4": "com.hulei.arcade.swipe.ball"
}


logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='new.log',
                    filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


def active_init():

    # clean the test result folder
    # get the current path
    current_path = os.path.split(os.path.realpath(__file__))[0]
    # get the folder uder current path
    current_filelist = os.listdir(current_path)
    # f should be a absolute path, if python is not run on current path
    for f in current_filelist:
        if os.path.isdir(os.path.join(current_path, f)):
            real_folder_path = os.path.join(current_path, f)
            try:
                for root, dirs, files in os.walk(real_folder_path):
                    for name in files:
                            # delete the log and test result
                        del_file = os.path.join(root, name)
                        os.remove(del_file)
                        logging.info(
                            '删除文件[%s] 成功' % name)
                shutil.rmtree(real_folder_path)
                logging.info(
                    '删除文件夹[%s] 成功' % f)
            except Exception:
                traceback.print_exc()


def compare_list(ad_type, table_dict, json_dict):
    '''这里获取表中对应的adtype的广告id，和json对比'''
    # table_dict = Table_Operation.get_adInfo_fromAdType()[1]
    # json_dict = Api_operation.get_Idinfo_fromJson()
    # if len(set(tablelist).difference(set(jsonlist))) > 0:
    #     index = tablelist.index(
    #         list(set(tablelist).difference(set(jsonlist)))[0]) + 1
    #     logging.error('对比表中数据存在不同，{}广告下第{}个广告不同,{}'.format(
    #         ad_type, index, set(tablelist).difference(set(jsonlist))))
    #     return False
    # return True
    table_dict = sorted(table_dict, key=lambda x: x["adID"])
    json_dict = sorted(json_dict, key=lambda x: x["adID"])
    for my_key in table_dict[0].keys():
        print(my_key)
        for index in range(len(table_dict)):
            value_eval = table_dict[index][str(my_key)]
            value_test = json_dict[index][str(my_key)]
            diff = difflib.SequenceMatcher(
                None, str(value_eval), str(value_test)).quick_ratio()
            if diff != 1.0:
                print("{}中，{}和{}的不同为:{} || {}".format(my_key,
                                                      'json_dict',
                                                      'table_dict',
                                                      value_test,
                                                      value_eval))
                logging.info("{}中，{}和{}的不同为:{} || {}".format(my_key,
                                                             'json_dict',
                                                             'table_dict',
                                                             value_test,
                                                             value_eval))
            else:
                print("{}和{}对比相同".format('json_dict', 'table_dict'))


if __name__ == '__main__':
    platform_index = input("请输入系统编号(IOS请打开vpn全局模式)- 1:IOS, 2:Android;")
    packname_index = input("请输入包名编号- 1:Tap, 2:Pop, 3:Doodle, 4:MakeBricks;")
    versionCode = input("请输入版本号-")

    active_init()

    Api_operation.Process_get_json(
        platform_dict[platform_index],
        packname_dict[packname_index],
        versionCode)
    # active_init()
    # Api_operation.Process_get_json(
    #     'android', 'com.pixel.art.coloring.by.number', '76')
    # compare_list('插屏')
    table_A, table_B = Table_Operation.get_adInfo_fromAdType(
        Table_Operation.get_excel_object()[0], 'rewardvideo')
    json_dict = Api_operation.get_Idinfo_fromJson()
    compare_list('rewardvideo', table_A, json_dict)
    os.system('pause')
