import subprocess
import os


# 封装adb 命令，返回结果为行数据
def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return [i.decode() for i in p.communicate()[0].splitlines()]


# adb 安装
def install(iPath, packagename):
    tag = os.popen("adb install -r {}\\{}".format(iPath, packagename)).read()
    return tag


# adb 查询版本信息
def inquiry_info(packagename):
    tag = os.popen(
        'adb shell pm dump {} | findstr "version"'.format(packagename)).read()
    return tag


# adb monkey的操作扩展
def monkey_go():
    pass


# adb 启动apk
def start_apk(packagename, launch_activity):
    tag = os.popen("adb shell am start -n %s" %
                   (packagename + "/" + launch_activity))
    return tag
