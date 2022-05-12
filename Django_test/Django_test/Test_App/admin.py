'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-10 12:29:28
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-05-12 14:05:09
'''
from django.contrib import admin

# Register your models here.
from Test_App.models import *


admin.site.register(Department)
admin.site.register(UserInfo)
admin.site.register(PhoneNumber)
