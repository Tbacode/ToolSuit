"""APITest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from MyApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', welcome),  # 进入主页
    path('home/', home),
    # re_path(r'^child/(?P<eid>.+)/(?P<oid>.*)/$', child),
    # path('child/<str:eid>/<str:oid>/', child),
    path('child/<str:eid>/<str:oid>/', child),
    path('login/', login),
    path('login_action/', login_action),
    path('register_action/', register_action),
    path('accounts/login/', login),
    path('logout/', logout),
    path('pei/', pei),  # 吐槽
    path('help/', api_help),  # 进入帮助文档
    path('project_list/', project_list),  # 进入项目列表
    path('delete_project/', delete_project),  # 删除项目
    path('add_project/', add_project),  # 新增项目
    path('apis/<str:id>/', open_apis),  # 进入接口库
    path('cases/<str:id>/', open_cases),  # 进入用例设置
    path('project_set/<str:id>/', open_project_set),  # 进入项目设置
]
