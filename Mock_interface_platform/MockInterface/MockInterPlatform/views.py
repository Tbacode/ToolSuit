'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-06-17 16:37:19
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-06-17 18:10:40
'''
import json
from django.shortcuts import render, HttpResponse

# Create your views here.

def mocklist(request):
    return render(request, 'layout.html')