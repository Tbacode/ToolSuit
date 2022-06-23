'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-06-17 16:37:19
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-06-23 17:25:23
'''
from django import forms
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from MockInterPlatform.models import Project, MockInterface
from MockInterPlatform.utils.pagenation import PageNation

# Create your views here.


def mocklist(request):
    # queryset = MockInterface.objects.all()
    project = Project.objects.all()

    data_dict = {}
    value = request.GET.get('q', "")  # 空字符串意思为，有q的值就拿，没有就是空
    if value:
        data_dict[
            'interface_name__contains'] = value  # 查找条件，包含value的interface_name字段

    queryset = MockInterface.objects.filter(**data_dict).order_by("-is_open")

    # 分页数据

    pageNationObject = PageNation(request, queryset)
    return render(
        request, 'mock_list.html', {
            "queryset": pageNationObject.page_queryset,
            "value": value,
            "project": project,
            "page_string": pageNationObject.html()
        })


def deleteinterface(request, nid):
    '''删除接口'''
    MockInterface.objects.filter(id=nid).delete()
    return redirect('/platform/list')


def editinterface(request, nid):
    '''修改接口'''
    project = Project.objects.all()
    row_obj = MockInterface.objects.filter(id=nid).first()
    if request.method == "GET":
        form = MockinterfaceEditModelForm(instance=row_obj)
        return render(request, "mock_edit.html", {
            "form": form,
            "project": project
        })
    # POST方式就是提交新增数据
    form = MockinterfaceEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/platform/list/")
    else:
        # 数据校验失败
        return render(request, 'mock_edit.html', {
            "form": form,
            "project": project
        })


# ******************* MockinterfaceAddModelForm *******************
class MockinterfaceAddModelForm(forms.ModelForm):

    class Meta:
        model = MockInterface
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_interface_name(self):
        interface_name = self.cleaned_data.get('interface_name')
        exists_name = MockInterface.objects.filter(interface_name=interface_name).exists()
        if exists_name:
            raise ValidationError("接口名称已存在")
    
        return interface_name


# ******************* end MockinterfaceAddModelForm *******************


# ******************* MockinterfaceEditModelForm *******************
class MockinterfaceEditModelForm(forms.ModelForm):

    class Meta:
        model = MockInterface
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    # 钩子函数，验证，编辑情况下，接口名是否重复
    def clean_interface_name(self):
        pk_id = self.instance.pk
        interface_name = self.cleaned_data.get('interface_name')

        exist_name = MockInterface.objects.exclude(id=pk_id).filter(
            interface_name=interface_name).exists()
        if exist_name:
            raise ValidationError("接口名称已存在")
        return interface_name


# ******************* end MockinterfaceEditModelForm *******************


def addinterface(request):
    ''' 新增mock接口 '''
    project = Project.objects.all()
    if request.method == "GET":
        form = MockinterfaceAddModelForm()
        return render(request, "mock_add.html", {
            "form": form,
            "project": project
        })
    # POST方式就是提交新增数据
    form = MockinterfaceAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/platform/list/")
    else:
        # 数据校验失败
        return render(request, 'mock_add.html', {
            "form": form,
            "project": project
        })
    # return render(request, 'mock_add.html')
