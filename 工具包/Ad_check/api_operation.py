# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-07-05 16:59:36
# @Last Modified by:   Tommy
# @Last Modified time: 2019-07-23 12:17:02
import json
import difflib
import requests
import os
from multiprocessing import Process, Queue


class Api_operation(object):
    '''封装好针对于广告API的操作'''
    def ad_check():
        '''查找广告配置中有是否存在不同数据以确认服务器是否存在AB分组配置'''
        f = open("com.pixel.art.coloring.by.number普通/groupA11.json",
                 encoding='utf-8')
        w = open("com.pixel.art.coloring.by.number普通/groupB11.json",
                 encoding='utf-8')

        x = json.load(f)
        y = json.load(w)
        for my_key in x["AdControl"].keys():
            print(my_key)
            for index in range(len(x["AdControl"][my_key])):
                x1 = sorted(x["AdControl"][my_key], key=lambda x: x["adID"])
                y1 = sorted(y["AdControl"][my_key], key=lambda x: x["adID"])

                for ad_key in x1[index].keys():
                    value_eval = x1[index][ad_key]
                    value_test = y1[index][ad_key]
                    diff = difflib.SequenceMatcher(
                        None, str(value_eval), str(value_test)).quick_ratio()
                    if diff != 1.0:
                        print("第{}个{}中，{}和{}的不同为:{} / {}".format(str(index + 1),
                                                                 ad_key,
                                                                 y["config"]["weightGroup"],
                                                                 x["config"]["weightGroup"],
                                                                 value_test,
                                                                 value_eval))

    def get_Adparam(platform, packname, visioncode, idfa_item, key):
        '''请求广告参数
        par: str,str,int
        return: dict
        '''
        url = 'http://ad.weplayer.cc/adInfo'

        data = {"platform": platform, "packageName": packname,
                "versionCode": visioncode, "idfa": idfa_item}

        headers = {"Content-Type": "application/json",
                   "Accept": "text/plain"}
        res = requests.post(
            url=url, data=json.dumps(data), headers=headers)
        res_init = json.dumps(res.json(), indent=2,
                              sort_keys=True, ensure_ascii=False)
        res_dict = json.loads(res_init)
        if not os.path.exists(packname + key):
            os.makedirs(packname + key)
        with open(packname + key + '/' + res_dict["config"]["weightGroup"] + '.json', "w") as f:
            json.dump(res_dict, f, indent=2)

    # 定义两个不同idfa的方法，以针对不同分组的广告配置，并用多进程运行
    def idfa_1234(Queue, platform, packname, visioncode, key):
        Api_operation.get_Adparam(
            platform, packname, visioncode, '1234', key)

    def idfa_123456(Queue, platform, packname, visioncode, key):
        Api_operation.get_Adparam(
            platform, packname, visioncode, '123456', key)

    def Process_get_json(platform, packname, visioncode):
        '''多进程获取广告配置，避免request的缓存问题导致json获取不全'''
        package_lastname = {"普通": "",
                            "美国": "-US",
                            "巴西": "-BR",
                            "印度": "-ID"}

        for key, item in package_lastname.items():
            q = Queue()
            p1 = Process(target=Api_operation.idfa_1234(Queue,
                                                        platform,
                                                        packname + item,
                                                        visioncode,
                                                        key), args=(q,))
            p2 = Process(target=Api_operation.idfa_123456(Queue,
                                                          platform,
                                                          packname + item,
                                                          visioncode,
                                                          key), args=(q,))
            p1.start()
            p2.start()
            p1.join()
            p2.join()

    def get_Idinfo_fromJson():
        # groupA_re_list = []
        with open('com.pixel.art.coloring.by.number普通/groupA11.json', 'r') as f:
            groupA = json.load(f)
            return groupA["AdControl"]["rewardvideo"]
            # for item in groupA["AdControl"]["rewardvideo"]:
            #     groupA_re_list.append(item["adID"])
            # return groupA_re_list


if __name__ == '__main__':
    # Api_operation.get_Adparam()
    # Api_operation.Process_get_json(
    #     'android', 'com.pixel.art.coloring.by.number', '76')
    print(Api_operation.ad_check())
