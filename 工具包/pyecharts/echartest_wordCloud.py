# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-16 15:58:52
# @Last Modified by:   Tommy
# @Last Modified time: 2019-05-16 18:11:57
from pyecharts import WordCloud
import os

name = [
    '呆子', '傻子', '笨比',
    '丑狗', '蠢货', '猥琐',
    '垃圾', '臭狗屎', '衣冠禽兽', '人品极差',
    '秃子', '丑骑兵', '丑东西', '地狱恶人', '口嗨王者'
]
value = [10000, 6189, 4556, 2356, 2233,
         1895, 1456, 1255, 981, 875,
         542, 462, 361, 265, 125]
worldcloud = WordCloud(width=1300, height=620)
worldcloud.add('狗棒子标签词云', name, value, word_size_range=[20, 100])
worldcloud.render('worldcloud01.html')
os.system('worldcloud01.html')
