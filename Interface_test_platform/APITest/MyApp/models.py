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
    name = models.CharField(max_length=30, null=True) # 超链接名字
    href = models.CharField(max_length=2000, null=True) # 超链接内容

    def __str__(self) -> str:
        return self.name

class DB_project(models.Model):
    name = models.CharField(max_length=100, null=True) # 项目名字
    remark = models.CharField(max_length=1000, null=True) # 项目备注
    user = models.CharField(max_length=15, null=True) # 项目创建者名字
    other_user = models.CharField(max_length=200, null=True) # 项目其他创建者名字

    def __str__(self) -> str:
        return self.name
