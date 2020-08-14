# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-07 17:11:07
# @Last Modified by:   Tommy
# @Last Modified time: 2019-05-15 12:24:08
import ftplib
import os


class Ftpoperation(object):
    # 初始化
    def __init__(self, host, user, pwd, acct, buffer_size):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.acct = acct
        self.buffer_size = buffer_size

    # 连接FTP服务器
    def connect(self):
        try:
            ftp = ftplib.FTP(self.host)
            ftp.login(self.user, self.pwd, self.acct)
            return ftp, '已连接到： "%s"' % self.host
        except ftplib.error_perm:
            return ftp, "FTP登陆失败，请检查主机号、用户名、密码、端口号是否正确"

    # 下载文件
    def download(self, ftp, filename):
        if not os.path.exists('包'):
            os.makedirs('包')
        if filename == "NULL":
            return False
        f = open('包/' + filename, 'wb').write
        try:
            ftp.retrbinary("RETR %s" % filename, f, self.buffer_size)
            return '成功下载文件："%s"' % filename + ',可在同级‘包’目录下查看安装包'

        except ftplib.error_perm:
            return False

    # 重定向
    def cwd_path(self, ftpconnectobj, path):
        try:
            ftpconnectobj.cwd(path)
            return True
        except ftplib.error_perm:
            return False
