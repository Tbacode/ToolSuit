from email.errors import MalformedHeaderDefect
from pyexpat import model
from django.db import models
from sqlalchemy import null, true

# Create your models here.


class DB_tucao(models.Model):
    user = models.CharField(max_length=30, null=True)  # 吐槽人名
    text = models.CharField(max_length=1000, null=True)  # 吐槽内容
    ctime = models.DateTimeField(auto_now=True)  # 创建时间

    def __str__(self):
        return '"' + self.text + '"' + "-" * 5 + str(self.ctime)


class DB_home_href(models.Model):
    name = models.CharField(max_length=30, null=True)  # 超链接名字
    href = models.CharField(max_length=2000, null=True)  # 超链接内容

    def __str__(self) -> str:
        return self.name


class DB_project(models.Model):
    name = models.CharField(max_length=100, null=True)  # 项目名字
    remark = models.CharField(max_length=1000, null=True)  # 项目备注
    user = models.CharField(max_length=15, null=True)  # 项目创建者名字
    other_user = models.CharField(max_length=200, null=True)  # 项目其他创建者名字

    def __str__(self) -> str:
        return self.name


class DB_apis(models.Model):
    project_id = models.CharField(max_length=10, null=True)  # 项目ID
    name = models.CharField(max_length=100, null=True)  # 接口名字
    api_method = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_login = models.CharField(max_length=10, null=True)  # 是否带登陆态
    api_host = models.CharField(max_length=100, null=True)  # 域名
    des = models.CharField(max_length=100, null=True)  # 描述
    body_method = models.CharField(max_length=20, null=True)  # 请求体编码格式
    api_body = models.CharField(max_length=1000, null=True)  # 请求体
    result = models.TextField(null=True)  # 返回体 因为长度巨大，所以用大文本方式存储
    sign = models.CharField(max_length=10, null=True)  # 是否验签
    file_key = models.CharField(max_length=50, null=True)  # 文件key
    file_name = models.CharField(max_length=50, null=True)  # 文件名
    public_header = models.CharField(max_length=1000, null=True)  # 全局变量-请求头

    last_body_method = models.CharField(max_length=20,null=True) # 上次请求体编码格式
    last_api_body = models.CharField(max_length=1000,null=True) # 上次请求体

    def __str__(self):
        return self.name
