'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-06-16 16:48:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-17 15:00:20
'''
from Base.base_request import request

url = 'https://tapcolor.weplayer.cc/normalApi/v1/getGalleryList'
data = {
    "game_ver": "6.7.4",
    "os_type": "Android",
    "register_date": "20210617",
    "register_ver": "6.7.4",
    "game_date": "20210617",
    "game_actDay": 1,
    "pic_type": "All",
    "start_date": "20210617",
    "group_id": 3,
    "hide_finish": 0,
}

res = request.run_main('get', url, data)
print(res)

