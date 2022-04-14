from imp import load_dynamic
from django.db import reset_queries
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MyApp.models import *
import json
import requests

# Create your views here.


@login_required
def welcome(request):
    # return HttpResponse('欢迎来到主页！！')
    return render(request, 'welcome.html')


# 返回子页面
def child(request, eid, oid):
    res = child_json(eid, oid)
    if eid == 'home.html':
        res = dict(res, **{"username": request.user.username})
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
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)
        res = {"project": project, "apis": apis}

    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}

    if eid == 'P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}
    return res


# 进入主页
@login_required
def home(request):
    return render(request, 'welcome.html', {
        "whichHTML": "home.html",
        "oid": "-1"
    })


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
    return render(request, 'welcome.html', {
        "whichHTML": "help.html",
        "oid": "-1"
    })


# 项目列表
def project_list(request):
    return render(request, 'welcome.html', {
        "whichHTML": "project_list.html",
        "oid": "-1"
    })


# 删除项目
def delete_project(request):
    id = request.GET['id']
    DB_project.objects.filter(id=id).delete()
    DB_apis.objects.filter(project_id=id).delete()
    return HttpResponse('')


# 新增项目
def add_project(request):
    project_name = request.GET['project_name']

    DB_project.objects.create(name=project_name,
                              remark='',
                              user=request.user.username,
                              other_user='')
    return HttpResponse('')


# 进入接口库
def open_apis(request, id):
    project_id = id
    return render(request, 'welcome.html', {
        "whichHTML": 'P_apis.html',
        "oid": project_id
    })


# 进入用例设置
def open_cases(request, id):
    project_id = id
    return render(request, 'welcome.html', {
        "whichHTML": 'P_cases.html',
        "oid": project_id
    })


# 进入项目设置
def open_project_set(request, id):
    project_id = id
    return render(request, 'welcome.html', {
        "whichHTML": 'P_project_set.html',
        "oid": project_id
    })


# 保存项目配置
def save_project_set(request, id):
    project_id = id
    name = request.GET['name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']

    DB_project.objects.filter(id=project_id).update(name=name,
                                                    remark=remark,
                                                    other_user=other_user)

    return HttpResponse('')


# 新增接口
def project_api_add(request, Pid):
    project_id = Pid
    DB_apis.objects.create(project_id=project_id, api_method='none')
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 删除接口
def project_api_del(request, id):
    # 根据接口ID找到对应的项目ID
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    # 根据项目ID删除该项目
    DB_apis.objects.filter(id=id).delete()
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 保存接口备注
def save_bz(request):
    api_id = request.GET['api_id']
    bz_value = request.GET['bz_value']
    DB_apis.objects.filter(id=api_id).update(des=bz_value)
    return HttpResponse('')


# 获取备注
def get_bz(request):

    api_id = request.GET['api_id']
    bz_value = DB_apis.objects.filter(id=api_id)[0].des
    return HttpResponse(bz_value)


# 保存接口
def Api_save(request):
    # 提取所有数据
    api_id = request.GET['api_id']
    api_name = request.GET['api_name']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']

    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
    else:
        ts_api_body = request.GET['ts_api_body']

    # 保存数据
    DB_apis.objects.filter(id=api_id).update(
        api_method=ts_method,
        api_url=ts_url,
        api_header=ts_header,
        api_host=ts_host,
        body_method=ts_body_method,
        api_body=ts_api_body,
        name=api_name,
    )
    # 返回
    return HttpResponse('success')


# 获取接口数据
def get_api_data(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type='application/json')


# 发送请求
def Api_send(request):
    # 提取所有数据
    api_id = request.GET['api_id']
    api_name = request.GET['api_name']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    print("****" * 10)
    print(ts_body_method)
    # ts_api_body = request.GET['ts_api_body']
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body

        if ts_body_method in ['', None]:
            return HttpResponse('请先选择好请求体编码格式和请求体内容，再点击Send按钮发送请求！')
    else:
        ts_api_body = request.GET['ts_api_body']
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)

    # 发送请求获取返回值
    header = json.loads(ts_header)  # 处理header字符格式

    # 处理拼接URL的异常情况
    if ts_host[-1] == '/' and ts_url[0] == '/':
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':
        url = ts_host + '/' + ts_url
    else:
        url = ts_host + ts_url

    if ts_body_method == 'none':
        response = requests.request(
            ts_method.upper(), url, headers=header, data={})
    elif ts_body_method == 'form-data':
        files = {}
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        response = requests.request(
            ts_method.upper(), url, headers=header, data=payload, files=files)
    elif ts_body_method == 'x-www-form-urlencoded':
        header['Content-Type'] = 'application/x-www-form-urlencoded'
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        print("****" * 10)
        print(payload)
        print("****" * 10)
        response = requests.request(
            ts_method.upper(), url, headers=header, data=payload)
    else:
        if ts_body_method == 'Text':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'JavaScript':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Json':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Html':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Xml':
            header['Content-Type'] = 'text/plain'
        response = requests.request(
            ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))
    # print(response)
    response = json.loads(response.text)
    response = json.dumps(response,indent=2)
    # print(type(response))

    # mock返回值
    return HttpResponse(response)


# 复制接口
def copy_api(request):
    api_id = request.GET['api_id']

    # 复制
    old_api = DB_apis.objects.filter(id=api_id)[0]

    DB_apis.objects.create(project_id=old_api.project_id,
                           name=old_api.name + '副本',
                           api_method=old_api.api_method,
                           api_url=old_api.api_url,
                           api_header=old_api.api_header,
                           api_login=old_api.api_login,
                           api_host=old_api.api_host,
                           des=old_api.des,
                           body_method=old_api.body_method,
                           api_body=old_api.api_body,
                           result=old_api.result,
                           sign=old_api.sign,
                           file_key=old_api.file_key,
                           public_header=old_api.public_header,
                           last_body_method=old_api.last_body_method,
                           last_api_body=old_api.last_api_body
                           )
    return HttpResponse('')
