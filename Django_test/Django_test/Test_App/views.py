from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
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


def user_list(request):

    queryset = UserInfo.objects.all()
    # 内容获取知识点
    # for obj in queryset:
    # 1. datetime转换
    #   obj.creat_time.strftime("%Y-%m-%d")
    # 2. choices 获取
    #   obj.gender -> 1\2
    #   obj.get_gender_display() ->1对应男，2对应女 get_属性名_display()
    # 3. 连表查询
    #   obj.depart_id -> id数据
    #   obj.depart.title -> id对应的表中title
    return render(request, 'user_list.html', {"queryset": queryset})


# ****************** UserModelForm ******************
class UserModelForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = [
            "name", "password", "age", "account", "creat_time", "depart",
            "gender"
        ]

    # 这里统一为展示的标签增加class属性，保留统一的样式
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # if name == 'password':
            #     field.widget.attrs = {"type": "password"}
            # elif name == "creat_time":
            #     field.widget.attrs = {"type": "Date"}
            field.widget.attrs = {"class": "form-control"}


# ****************** end UserModelForm ******************


def user_add(request):
    ''' 用户新增 '''
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})

    # POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # print(form.cleaned_data)
        # UserInfo.object.creat(......) 可以保存，但是不推荐
        # form.sava()实际是保存输入的所有内容，如果在输入内容上
        # 存在其他要保存到数据库中的数据可以用下面的方法新增
        # from.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    else:
        # 校验失败，显示错误信息
        return render(request, 'user_add.html', {"form": form})


def user_edit(request, nid):
    ''' 用户编辑 '''
    row_obj = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # row_obj = UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {"form": form})

    # 这里用ModelForm更新表，需要加入更新对象，不然就是新增
    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    ''' 删除用户 '''
    # 操作数据库，对id相同的进行删除
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def phone_list(request):
    ''' 靓号列表 '''
    data_dict = {}
    value = request.GET.get('q', "")  # 空字符串意思为，有q的值就拿，没有就是空
    if value:
        data_dict['mobile__contains'] = value

    # 分页数据
    page = int(request.GET.get('page', 1))
    start = (page - 1) * 10
    end = page * 10

    # 当字典为空的时候，就相当于注释内容的all()，不为空就是筛选查找
    queryset = PhoneNumber.objects.filter(
        **data_dict).order_by("level")[start:end]
    # print(res)
    # queryset = PhoneNumber.objects.all().order_by("level")
    return render(request, 'phone_list.html', {
        "queryset": queryset,
        "value": value
    })


# ****************** PhoneModelForm ******************
class PhoneModelForm(forms.ModelForm):
    mobile = forms.CharField(label="手机号",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}', '手机号格式错误'),
                             ])

    class Meta:
        model = PhoneNumber
        # fields = ["mobile", "price", "level", "status"]
        fields = "__all__"

    # 这里统一为展示的标签增加class属性，保留统一的样式
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # if name == 'password':
            #     field.widget.attrs = {"type": "password"}
            # elif name == "creat_time":
            #     field.widget.attrs = {"type": "Date"}
            field.widget.attrs = {"class": "form-control"}

    # 钩子方法，字段验证

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exist_mobile = PhoneNumber.objects.filter(mobile=txt_mobile).exists()
        if exist_mobile:
            raise ValidationError("手机号已经存在")
        return txt_mobile


# ****************** end PhoneModelForm ******************


# ****************** PhoneEditModelForm ******************
class PhoneEditModelForm(forms.ModelForm):
    mobile = forms.CharField(disabled=True)  # 显示但是不可编辑

    class Meta:
        model = PhoneNumber
        # fields = ["mobile", "price", "level", "status"]
        fields = "__all__"

    # 这里统一为展示的标签增加class属性，保留统一的样式
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # if name == 'password':
            #     field.widget.attrs = {"type": "password"}
            # elif name == "creat_time":
            #     field.widget.attrs = {"type": "Date"}
            field.widget.attrs = {"class": "form-control"}

    # 钩子方法：在编辑时，排除自身去验证字段重复
    def clean_mobile(self):
        # 当前编辑的那一行的ID ，其实就是该对象的主键pk。
        # 因为实例化该类时，传入了instance，代表的row_obj对象
        pk_id = self.instance.pk
        txt_mobile = self.cleaned_data['mobile']
        # 判断是不是当前修改ID，但是号码相同的数据，是否存在
        exist_mobile = PhoneNumber.objects.exclude(id=pk_id).filter(
            mobile=txt_mobile).exists()
        if exist_mobile:
            raise ValidationError("手机号已经存在")
        return txt_mobile


# ****************** end PhoneEditModelForm ******************


def phone_add(request):
    ''' 靓号添加 '''
    if request.method == "GET":
        form = PhoneModelForm()
        return render(request, 'phone_add.html', {"form": form})
    form = PhoneModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/phone/list/')
    else:
        return render(request, 'phone_add.html', {"form": form})


def phone_edit(request, nid):
    ''' 靓号编辑 '''
    row_obj = PhoneNumber.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PhoneEditModelForm(instance=row_obj)
        return render(request, 'phone_edit.html', {"form": form})

    form = PhoneEditModelForm(instance=row_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/phone/list')
    else:
        return render(request, 'phone_edit.html', {"form": form})


def phone_delete(request, nid):
    ''' 靓号删除 '''
    PhoneNumber.objects.filter(id=nid).delete()
    return redirect('/phone/list/')


def panel(request):
    # return redirect('http://127.0.0.1:3000/d/5iilUVjnz/grafana_test?orgId=1&from=1654768800000&to=now&refresh=1s&kiosk')
    return render(request, 'iframe.html')





