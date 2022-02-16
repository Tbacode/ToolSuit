'''
 * @Descripttion : Gallery数据替换掉Recommend构建测试数据
 * @Author       : Tommy
 * @Date         : 2022-02-12 17:19:16
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-02-12 18:02:19
'''

import requests
import json


def request_function(url: str, data: dict, method: str = "get") -> dict:
    if method != "get":
        res = requests.post(url=url, data=data).text
    else:
        res = requests.get(url=url, params=data).text

    return json.loads(res)


def galleryData_exchange(data: list) -> dict:
    for data_item in data:
        del data_item['picSettings']
        del data_item['picExtraType']
    return json.dumps(data)
    # return data


if __name__ == "__main__":
    url_gallery = r"https://tapcolor-lite-dev.taplayer.net/normalApi/v1/getGalleryList"
    params = {
        "os_type": "Android",
        "game_ver": "5.5.0",
        "register_ver": "5.5.0",
        "register_date": "20220212",
        "game_date": "20220212",
        "game_actDay": 1,
        "u_af_status": "Organic",
        "pic_type": "All",
        "start_date": "20220212",
        "hide_finish": 0,
        "group_id": 25,
        "ignore_child_logic": 0
    }
    res = request_function(url_gallery, params)
    res = galleryData_exchange(res['data']['picList'])
    print(len(list(res)))

