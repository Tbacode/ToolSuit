'''
Author: your name
Date: 2022-04-06 11:16:09
LastEditTime: 2022-04-08 19:43:34
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \APITest\MyApp\views.py
'''
from os import name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MyApp.models import *


# Create your views here.

@login_required
def welcome(request):
    # return HttpResponse('欢迎来到主页！！')
    return render(request, 'welcome.html')

# 返回子页面
def child(request, eid, oid):
    res = child_json(eid, oid)
    return render(request, eid, res)

# 控制不同的页面返回不同的数据：数据分发器
def child_json(eid, oid=''):
    res = {}
    if eid == 'home.html':
        data = DB_home_href.objects.all()

        res = {"hrefs": data}
    if eid == 'project_list.html':
        data = DB_project.objects.all()
        res = {"projects": data}

    if eid == 'P_apis.html':
        project_name = DB_project.objects.filter(id=oid)[0].name
        res = {"project_name":project_name}
    return res

# 进入主页
@login_required
def home(request):
    return render(request, 'welcome.html', {"whichHTML": "home.html", "oid": "-1"})


# 退出登录
def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def login(request):
    return render(request, 'login.html')


# 登录开始
def login_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']

    # 验证用户
    from django.contrib import auth
    user = auth.authenticate(username=u_name, password=p_word)

    if user is not None:
        # return HttpResponseRedirect('/home/')
        auth.login(request, user)
        request.session['user'] = u_name
        return HttpResponse('成功')
    else:
        # 用户验证失败
        return HttpResponse('失败')


# 注册
def register_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']

    from django.contrib.auth.models import User

    try:
        user = User.objects.create_user(username=u_name, password=p_word)
        user.save()
        return HttpResponse('注册成功')
    except:
        return HttpResponse('注册失败！用户名好像已经存在了')


# 吐槽
def pei(request):
    tucao_text = request.GET['tucao_text']
    DB_tucao.objects.create(user=request.user.username, text=tucao_text)

    return HttpResponse('')


# 帮助
def api_help(request):
    return render(request, 'welcome.html', {"whichHTML": "help.html", "oid": "-1"})


# 项目列表
def project_list(request):
    return render(request, 'welcome.html', {"whichHTML": "project_list.html", "oid": "-1"})


# 删除项目
def delete_project(request):
    id = request.GET['id']
    DB_project.objects.filter(id=id).delete()
    return HttpResponse('')


# 新增项目
def add_project(request):
    project_name = request.GET['project_name']

    DB_project.objects.create(name=project_name,remark='',user=request.user.username,other_user='')
    return HttpResponse('')


# 进入接口库
def open_apis(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": 'P_apis.html', "oid": project_id})


# 进入用例设置
def open_cases(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": 'P_cases.html', "oid": project_id})


# 进入项目设置
def open_project_set(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": 'P_project_set.html', "oid": project_id})