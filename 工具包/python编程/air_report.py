'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2020-08-14 11:18:16
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-07-28 14:45:43
'''
import zipfile
import os
import requests
import shutil


def report_zip():
    startdir = r"C:\Users\xt875\Desktop\airtest_file\report\BBB_airtest.log\static"  #要压缩的文件夹路径
    file_news = startdir + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(
            r"C:\Users\xt875\Desktop\airtest_file\report\BBB_airtest.log",
            '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
            # z.write(os.path.join(dirpath, filename))
            print('压缩成功')
    z.close()


def report_zip_append():
    zip_dir = r"C:\Users\xt875\Desktop\airtest_file\report\BBB_airtest.log\static.zip"  # 压缩文件夹路径
    file_news = r"C:\Users\xt875\Desktop\airtest_file\report\BBB_airtest.log\log.html"
    file_news2 = r"C:\Users\xt875\Desktop\airtest_file\report\BBB_airtest.log\log"
    z = zipfile.ZipFile(zip_dir, 'a', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(file_news2):
        fpath = dirpath.replace(
            r"C:\Users\xt875\Desktop\airtest_file\report\BBB_airtest.log",
            '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
            # z.write(os.path.join(dirpath, filename))
            print('压缩成功')
    basename = os.path.basename(file_news)
    z.write(file_news, basename, zipfile.ZIP_DEFLATED)


# 传入文件
def post_file(id_url, wx_url, file):
    data = {'file': open(file, 'rb')}
    # 请求id_url(将文件上传微信临时平台),返回media_id
    # id_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=xxx&type=file'
    response = requests.post(url=id_url, files=data)
    json_res = response.json()
    media_id = json_res['media_id']

    data = {"msgtype": "file", "file": {"media_id": media_id}}
    result = requests.post(url=wx_url, json=data)
    return (result)


# 删除log文件资源
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            shutil.rmtree(c_path, True)
        else:
            os.remove(c_path)


if __name__ == "__main__":
    # report_zip()
    # report_zip_append()
    file1 = r'C:\Users\xt875\Desktop\airtest_file\log'  # 文件路径
    id_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=eef716ba-a7e2-423e-9c9a-7cac807e397c&type=file'  # 把机器人的key放入
    wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=eef716ba-a7e2-423e-9c9a-7cac807e397c'  # 把机器人的key放入
    res = post_file(id_url, wx_url, file=r"C:\Users\xt875\Desktop\airtest_file\report\BBB_airtest.log\static.zip")
    if res.status_code == 200:
        log_path = r"C:\Users\xt875\Desktop\airtest_file\log"
        report_path = r"C:\Users\xt875\Desktop\airtest_file\report"
        del_file(log_path)
        del_file(report_path)