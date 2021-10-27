'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-09-03 17:38:07
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-10-27 17:45:23
'''
import requests
from handle_excel import excel

data = excel.get_columns_values("A")

for item_index in range(1, len(data)):
    if data[item_index] is not None:
        url = r"https://gcp-cdn.tapcolor.taplayer.net/debug/1.0/Thumbnails/{}.png".format(data[item_index])
        res = requests.get(url=url)
        if res.status_code != 200:
            print(data[item_index])



# https://gcp-cdn.tapcolor.taplayer.net/debug/1.0/Thumbnails/pic_-O4zLSSrWW.png
