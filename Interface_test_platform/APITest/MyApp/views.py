'''
Author: your name
Date: 2022-04-06 11:16:09
LastEditTime: 2022-04-06 18:27:05
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \APITest\MyApp\views.py
'''
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

def welcome(request):
    print("进来主页了")
    # return HttpResponse('欢迎来到主页！！')
    return render(request, 'welcome.html')

# 返回子页面


def child(request, eid, oid):
    print("进入子页面了")
    print(eid)
    print(oid)
    return render(request, eid, {"username": oid})


def home(request):
    return render(request, 'welcome.html', {"whichHTML": "home.html", "oid": "航宝宝"})
