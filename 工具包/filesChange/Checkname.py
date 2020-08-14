# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-06-26 14:49:57
# @Last Modified by:   Tommy
# @Last Modified time: 2019-11-06 16:58:41
import os
import shutil
from PIL import Image
import numpy as np
path = r"C:\Users\xt875\Documents\Pictures\TapColor\Pictures\1步-等待机器预配置的图\第二批美术图片\刘聪"
# path = "C:\\Users\\xt875\\Desktop\\1"
# path = "lala"
copypath = 'C:\\Users\\xt875\\Desktop\\copydir'


# 返回当前path下的文件夹名称：list
def get_files_name(path, traverse=False):
    # file_list = []
    for root, dirs, files in os.walk(path):
        if not traverse:
            return root, dirs, files


# 返回指定后缀的文件名
def get_filesname_by_suffixes(path, suffixe='npic', traverse=False):
    name_list = []
    for root, dirs, files in os.walk(path):
        if not traverse:
            for file in files:
                file_suffix = os.path.splitext(file)[1][1:].lower()
                if file_suffix in suffixe:
                    name_list.append(os.path.splitext(file)[0][:])
    return name_list


# 返回文件夹内的详细文件
def get_filesname(path, path_dirslist):
    for dir in path_dirslist:
        print("[" + dir + "]" + "文件夹下的详细信息：")
        path_filename = os.path.join(path, dir)
        for root, dirs, files in os.walk(path_filename):
            for file in files:
                path_img = os.path.join(path_filename, file)
                keyword = str(get_img_size(
                    os.path.join(path_filename, file))[0])
                print("----{}的大小是: {} KB,尺寸大小:{},尺寸是否符合名称: {} ".format(
                    file, get_img_volume(path_img),
                    get_img_size(path_img),
                    isfilename_include_keyword(file, keyword)))
            print("----文件夹下文件数量：" + str(len(files)))


# 返回文件夹内是否包含关键字
def isfilename_include_keyword(filename, keyword):
    if keyword in filename:
        return True
    else:
        return False


# 修改错误的名字和文件夹名字相同
def file_rename(path, dirname, filename):
    os.rename(path + "\\" + filename + ".npic",
              path + "\\" + dirname + ".npic")


# 创建文件夹，放置目标文件
def get_file_in_dir(path, filename, suffixe='npic'):
    if not os.path.exists(copypath):
        os.makedirs(copypath)
    oldfile = path + '\\' + filename + '.' + suffixe
    newfile = copypath + '\\' + filename + '.' + suffixe
    shutil.copyfile(oldfile, newfile)


# 返回修改完的文件
def return_change_file(copypath, path, filename, suffixe='npic'):
    if os.access(copypath + "\\" + filename + '.' + suffixe, os.F_OK):
        oldfile = copypath + '\\' + filename + '.' + suffixe
        newfile = path + '\\' + filename + '\\' + filename + '.' + suffixe
        shutil.copyfile(oldfile, newfile)


# 判断是否纹理图
def judeg_img_type(file_list):
    for file in file_list:
        if "jpg" in file:
            return True
    return False


# 获取图片尺寸
def get_img_size(path_img):
    try:
        img_object = Image.open(path_img)
    except OSError as e:
        return "非图片文件"
    img_width, img_heigh = img_object.size[0], img_object.size[1]
    return img_width, img_heigh


# 获取文件大小
def get_img_volume(path_file):
    try:
        size = os.path.getsize(path_file)
        return formatSize(size)
    except Exception as err:
        print(err)


# 文件大小转换KB
def formatSize(size_bytes):
    try:
        bytes = float(size_bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    return int(kb)


# 判断是否是彩色线框图
def judge_img_iscolor(path_dir, img_list):
    flag = True
    for img in img_list:
        img = img + '.png'
        img_pilobect = Image.open(os.path.join(path_dir, img))
        if not isGrayMap(img_pilobect):
            flag = False
            break
    return flag


# 黑白照片（灰度图）识别
def isGrayMap(img, threshold=5):
    """
    入参：
    img：PIL读入的图像
    threshold：判断阈值，图片3个通道间差的方差均值小于阈值则判断为灰度图。
    阈值设置的越小，容忍出现彩色面积越小；设置的越大，那么就可以容忍出现一定面积的彩色，例如微博截图。
    如果阈值设置的过小，某些灰度图片会被漏检，这是因为某些黑白照片存在偏色，例如发黄的黑白老照片、
    噪声干扰导致灰度图不同通道间值出现偏差（理论上真正的灰度图是RGB三个通道的值完全相等或者只有一个通道，
    然而实际上各通道间像素值略微有偏差看起来仍是灰度图）
    出参：
    bool值
    """
    if len(img.getbands()) == 1:
        return True
    img1 = np.asarray(img.getchannel(channel=0), dtype=np.int16)
    img2 = np.asarray(img.getchannel(channel=1), dtype=np.int16)
    img3 = np.asarray(img.getchannel(channel=2), dtype=np.int16)
    diff1 = (img1 - img2).var()
    diff2 = (img2 - img3).var()
    diff3 = (img3 - img1).var()
    diff_sum = (diff1 + diff2 + diff3) / 3.0
    if diff_sum <= threshold:
        return True
    else:
        return False


if __name__ == "__main__":
    # img_path = r"C:\Users\xt875\Documents\Pictures\TapColor\Pictures\1步-等待机器预配置的图\第二批美术图片\纹理图"
    dir_list = get_files_name(path)[1]
    get_filesname(path, dir_list)
    # dirslist = get_files_name(path)
    # for dir in dirslist:
    #     filename = get_filesname_by_suffixes(path + '\\' + dir)[0]
    #     if filename:
    #         if dir == filename:
    #             # print("文件夹名：" + str(dir) + "和npic文件名：" + str(filename) + "相同")
    #             get_file_in_dir(path + '\\' + dir, filename)
    #         else:
    #             print("路径" + path + '\\' + dir +
    #                   "下的npic文件名称与文件夹名称不同")
    #             file_rename(path + '\\' + dir, dir, filename)
    #     else:
    #         print("路径" + path + '\\' + dir + "下的文件不完整")
    # os.system("pause")
    # for dir in dirslist:
    #     return_change_file(copypath, path, dir)
    #     print("放回npic文件：{}".format(dir))
