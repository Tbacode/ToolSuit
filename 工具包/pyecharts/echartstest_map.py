# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-16 15:45:40
# @Last Modified by:   Tommy
# @Last Modified time: 2019-05-16 15:56:22
'''
 安装下列地图数据包
 pip install echarts-countries-pypkg
 pip install echarts-china-provinces-pypkg
 pip install echarts-china-cities-pypkg
 pip install echarts-china-counties-pypkg
 pip install echarts-china-misc-pypkg
 pip install echarts-united-kingdom-pypkg
'''
from pyecharts import Map


value = [155, 10, 66, 78]
attr = ['福建', '山东', '北京', '上海']
map = Map('全国地图示例', width=1200, height=600)
map.add('', attr, value, maptype='china')
map.render('map01.html')


value = [155, 10, 66, 78]
attr = ['成都市', '绵阳市', '德阳市', '广元市']
map = Map('四川地图实例', width=1200, height=600)
map.add('', attr, value, maptype='四川',
        is_visualmap=True,
        visual_text_color='#000',
        is_label_show=True
        )
map.render('map02.html')
