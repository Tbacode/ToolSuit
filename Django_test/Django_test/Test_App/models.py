'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-10 12:29:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-05-11 18:23:17
'''
from django.db import models

# Create your models here.


class Department(models.Model):
    ''' 部门表 '''
    title = models.CharField(verbose_name='标题', max_length=32)
    docs = models.CharField(verbose_name="描述", max_length=100, default="描述")

    def __str__(self) -> str:
        return self.title


class UserInfo(models.Model):
    ''' 员工表 '''
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    # 总长度为10位，小数位占2
    account = models.DecimalField(
        verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # creat_time = models.DateTimeField(verbose_name='入职时间')
    creat_time = models.DateField(verbose_name='入职时间')
    # 无约束
    # depart_id = models.IntegerField(verbose_name='部门id')
    # 有约束
    #   - to, 与哪张表关联（外键）
    #   - to_field, 与表中哪一列关联
    # 在django中
    #   - ForeignKey的变量定义，在生成数据列时，自动增加“_id”
    # 如果部门被删除，
    #   - 用户也删除：级联删除
    depart = models.ForeignKey(
        verbose_name="部门", to='Department', to_field='id', on_delete=models.CASCADE)
    #   - 置空，但是要确保该字段可以为空
    # depart = models.ForeignKey(
    #     to='Department', to_field='id', on_delete=models.SET_NULL, null=True, blank=True)

    # 在Django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(
        verbose_name="性别", choices=gender_choices)
