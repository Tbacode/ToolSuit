# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-07-05 15:37:27
# @Last Modified by:   Tommy
# @Last Modified time: 2019-07-11 15:57:08
# import hashlib


# def getHash(f):
#     line = f.readline()
#     hash = hashlib.md5()
#     while (line):
#         hash.update(line)
#         line = f.readline()
#     return hash.hexdigest()


# def IsHashEqual(f1, f2):
#     str1 = getHash(f1)
#     print(str1)
#     str2 = getHash(f2)
#     print(str2)
#     return str1 == str2


# if __name__ == '__main__':
#     f1 = open("1.json", "rb")
#     f2 = open("2.json", "rb")
#     print(IsHashEqual(f1, f2))
# import json as js
# import difflib

# f = open("1.json", encoding='utf-8')
# w = open("2.json", encoding='utf-8')

# x = js.load(f)
# y = js.load(w)

# for my_key in x["AdControl"].keys():
#     print(my_key)
#     for index in range(len(x["AdControl"][my_key])):

#         for ad_key in x["AdControl"][my_key][index].keys():
#             value_eval = x["AdControl"][str(my_key)][index][ad_key]
#             value_test = y["AdControl"][str(my_key)][index][ad_key]
#             diff = difflib.SequenceMatcher(
#                 None, str(value_eval), str(value_test)).quick_ratio()
#             if diff != 1.0:
#                 print("第{}个{}中，{}和{}的不同为:{} / {}".format(str(index + 1),
#                                                          ad_key,
#                                                          y["config"]["weightGroup"],
#                                                          x["config"]["weightGroup"],
#                                                          value_test,
#                                                          value_eval))
# import os
# import shutil
# import traceback
# import logging


# def misc_init():
#     logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
#                         filename='new.log',
#                         filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
#                         # a是追加模式，默认如果不写的话，就是追加模式
#                         format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
#                         # 日志格式
#                         )
#     # clean the test result folder
#     # get the current path
#     current_path = os.path.split(os.path.realpath(__file__))[0]
#     # get the folder uder current path
#     current_filelist = os.listdir(current_path)
#     # f should be a absolute path, if python is not run on current path
#     for f in current_filelist:
#         if os.path.isdir(os.path.join(current_path, f)):
#             real_folder_path = os.path.join(current_path, f)
#             try:
#                 for root, dirs, files in os.walk(real_folder_path):
#                     for name in files:
#                             # delete the log and test result
#                         del_file = os.path.join(root, name)
#                         os.remove(del_file)
#                         logging.info(
#                             '删除文件[%s] 成功' % name)
#                 shutil.rmtree(real_folder_path)
#                 logging.info(
#                     '删除文件夹[%s] 成功' % f)
#             except Exception:
#                 traceback.print_exc()


# misc_init()
# def compare_list(ad_type):
#     tablelist = ['682072852175616_851618791887687', 'ca-app-pub-9240980261558928/3393678932', '5cc53ed573c8aa00115f90cd$INTERSTITIAL_001-9008978', '7c08ecaff7d1405388d6795ead6edfa2', '5cc53ed573c8aa00115f90cd$NEW_INTERSTITIAL_001-4222144', '682072852175616_851619031887663', 'ca-app-pub-9240980261558928/8834488124',
#                  '5cc53ed573c8aa00115f90cd$INTERSTITIAL_002-9641026', '379b186ab7a248d792d3acd878a9ee9c', '682072852175616_851619208554312', 'ca-app-pub-9240980261558928/4172763358', '5cc53ed573c8aa00115f90cd$INTERSTITIAL_003-0335063', '19bdc4c7c8044fb5be50794f73e52a88', '682072852175616_851619328554300']
#     jsonlist = ['5cc53ed573c8aa00115f90cd$INTERSTITIAL_001-9008978', '7c08ecaff7d1405388d6795ead6edfa2', '5cc53ed573c8aa00115f90cd$NEW_INTERSTITIAL_001-4222144', '5cc53ed573c8aa00115f90cd$INTERSTITIAL_002-9641026', '379b186ab7a248d792d3acd878a9ee9c', '5cc53ed573c8aa00115f90cd$INTERSTITIAL_003-0335063',
#                 '19bdc4c7c8044fb5be50794f73e52a88', '682072852175616_851618791887687', 'ca-app-pub-9240980261558928/3393678932', '682072852175616_851619031887663', 'ca-app-pub-9240980261558928/8834488124', '682072852175616_851619208554312', 'ca-app-pub-9240980261558928/4172763358', '682072852175616_851619328554300']
#     print(set(tablelist).difference(set(jsonlist)))


# compare_list('ad')

import difflib

a = {"x": 1, "y": 2, "z": 3, "w": 4}
b = {"x": 1, "y": 2, "z": 3, "b": 4}

print(a.items() & b.items())


json_dict = {"banner": [
    {
        "adID": "ca-app-pub-9240980261558928/4657529848",
        "channel": "Admob8",
        "loader": "4",
        "weight": 10,
        "Cover": False,
        "interval": 60,
        "subloader": "2",
        "ecpm": 4
    },
    {
        "adID": "ca-app-pub-9240980261558928/1564462645",
        "channel": "Admob7",
        "loader": "3",
        "weight": 10,
        "Cover": False,
        "interval": 60,
        "subloader": "3",
        "ecpm": 3
    },
    {
        "adID": "ca-app-pub-9240980261558928/7746727618",
        "channel": "Admob6",
        "loader": "2",
        "weight": 10,
        "Cover": False,
        "interval": 60,
        "subloader": "4",
        "ecpm": 2
    }
]
}

table_dict = {"banner": [
    {
        "adID": "ca-app-pub-9240980261558928/4657529848",
        "channel": "Admob8",

    },
    {
        "adID": "ca-app-pub-9240980261558928/7746727618",
        "channel": "Admob6",

    },
    {
        "adID": "ca-app-pub-9240980261558928/15644626454",
        "channel": "Admob7",

    },

]
}
table_dict = sorted(table_dict["banner"], key=lambda x: x["adID"])
json_dict = sorted(json_dict["banner"], key=lambda x: x["adID"])
# for index in range(len(json_dict["banner"])):
#     a = (json_dict["banner"][index]).items() & (
#         table_dict["banner"][index]).items()
#     print(a)
# table_dict = sorted(table_dict, key=lambda x: table_dict["banner"][0].keys())
# print(table_dict)
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
