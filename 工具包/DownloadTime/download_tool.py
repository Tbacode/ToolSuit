'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-01-07 17:16:05
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-01-08 16:54:21
'''
import requests


class DownloadTool(object):
    def __init__(self, url):
        self.url = url

    # TODO: 下载数据
    def download_file(self, filename):
        self.r = requests.get(self.url, stream=True)
        with open("resource/" + filename, "wb") as code:
            for chunk in self.r.iter_content(chunk_size=1024000):
                if chunk:
                    code.write(chunk)
