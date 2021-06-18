'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-06-16 16:48:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-18 14:31:38
'''
from Base.base_request import request

url = '/normalApi/v1/getDiscount/'
data = {
    "game_ver": "6.7.5",
    "os_type": "Android",
    "register_date": "20210617",
    "register_ver": "6.7.5",
    "game_date": "20210617",
    "game_actDay": 5,
    "is_vip": 0,
    "type": "subscribe"
}

res = request.run_main('get', url, data, 'debugcolorhost')
print(res)
