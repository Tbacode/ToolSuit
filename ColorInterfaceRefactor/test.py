'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-06-16 16:48:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-22 14:17:24
'''
# from Base.base_request import request
# import json

# url = '/content/'
# data = {
#     "game_ver": "6.7.5",
#     "os_type": "Android",
#     "register_date": "20210617",
#     "register_ver": "6.7.5",
#     "game_date": "20210617",
#     "game_actDay": 5,
#     "is_vip": 0,
#     "type": "subscribe"
# }
# data1 = {
#     "app_version": "2.9.1",
#     "package_name": "com.pixel.art.coloring.color.number",
#     "os_name": "android",
#     "os_version": "22",
#     "user_id": "c6c9feb7-d8ea-4d8f-a943-379cb34ee6f1",
#     "limit_tracking": "0",
#     "api_content_version": "4.3.1",
#     "utc": "8",
#     "level_quality": "high",
#     "lang": "ChineseSimplified",
#     "country": "CN",
#     "icon_quality": "low",
#     "app_layout": "phone",
#     "time": "1624285846",
#     "install_date": "1623750414",
#     "page": "1",
#     "solve_page_treasure_status": "2",
#     "auto_select_color_status": "2",
#     "palette_color_progress_status": "1",
#     "reward_lock_pictures_status": "2",
# }

# res = request.run_main('post', url, data1, 'flowhost')
# print(type(res))
# # print(res)
# with open('test.json', 'w', encoding='utf-8') as f:
#     res = json.dumps(res)
#     f.write(res)
string = '{"os_type":"Android","game_ver":"6.7.5","register_ver":"6.7.5","register_date":"20210617","game_date": {1},"game_actDay":1,"group_id":63}'
string = eval(string)
string['game_date'] = "111111111"
print(string)
