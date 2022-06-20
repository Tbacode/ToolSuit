from django.db import models


# Create your models here.
class Project(models.Model):
    ''' 项目表 '''
    pro_name = models.CharField(verbose_name='项目名称', max_length=32)

    def __str__(self) -> str:
        return self.pro_name


class MockInterface(models.Model):
    ''' Mock接口信息表 '''
    interface_name = models.CharField(verbose_name="接口名称", max_length=50)
    interface_url = models.CharField(verbose_name="接口地址", max_length=64)
    request_parms = models.CharField(verbose_name="请求参数", max_length=200, default="")
    # 约束条件
    is_open_choices = ((1, "开"), (0, "关"))
    is_open = models.SmallIntegerField(verbose_name="是否打开",
                                       choices=is_open_choices)
    response = models.CharField(verbose_name="返回信息", max_length=500)
    method = models.CharField(verbose_name="请求方式", max_length=10)
    project = models.ForeignKey(verbose_name="项目名称",
                                to='Project',
                                to_field='id',
                                on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.interface_name