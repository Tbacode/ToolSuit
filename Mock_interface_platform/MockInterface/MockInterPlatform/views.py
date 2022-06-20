
from django.shortcuts import redirect, render
from MockInterPlatform.models import Project, MockInterface

# Create your views here.


def mocklist(request):
    queryset = MockInterface.objects.all()
    project = Project.objects.all()
    return render(request, 'mock_list.html', {
        "queryset": queryset,
        "project": project
    })


def deleteinterface(request, nid):
    '''删除接口'''
    MockInterface.objects.filter(id=nid).delete()
    return redirect('/platform/list')


def editinterface(request, nid):
    '''修改接口'''
    inter_id = request.GET.get("nid")
    queryset = MockInterface.objects.filter(id=inter_id).first()
    return render(request, 'mock_edit.html', {"queryset": queryset})