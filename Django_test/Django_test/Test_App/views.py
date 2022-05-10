from turtle import title
from django.shortcuts import redirect, render
from Test_App.models import *

# Create your views here.


def depart_list(request):
    '''部门列表'''

    # 1.获取部门列表从数据库中
    departlist = Department.objects.all()
    return render(request, "depart_list.html", {"depart_list": departlist})


def depart_add(request):
    ''' 添加部门 '''
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # else就是提交数据
    title = request.POST.get('title')
    Department.objects.create(title=title)

    # 保存数据后，重定向到部门列表
    return redirect('/depart/list/')


def depart_delete(request):
    ''' 删除部门 '''
    # 获取要删除的部门ID
    depart_id = request.GET.get('nid')
    # 操作数据库，对id相同的进行删除
    Department.objects.filter(id=depart_id).delete()
    return redirect('/depart/list/')


def depart_edit(request, nid):
    ''' 修改部门 '''
    if request.method == "GET":
        row_object = Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})

    title = request.POST.get('title')
    Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')
