'''
 * @Descripttion : 封装对于爬虫行为的操作
 * @Author       : Tommy
 * @Date         : 2021-05-12 17:17:39
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-07 17:10:20
'''
from fake_useragent import UserAgent
from threading import Thread, Lock
from queue import Queue
from lxml import etree
import requests
from bs4 import BeautifulSoup
import time
import random
from loguru import logger


class HandleSpider(object):
    def __init__(self):
        '''
         * @name: Tommy
         * @msg: HandleExcel 初始化
         * @param {初始化url,headers}
         * @return {*}
        '''
        self.headers = {'User-Agent': UserAgent().random}
        logger.debug("User-Agent：" + str(self.headers))
        # 创建url队列、线程锁
        self.url_queue = Queue()
        self.lock = Lock()

    def get_html(self, url):
        '''
         * @name: Tommy
         * @msg: 获取html页面内容
         * @param {*}
         * @return {*}
        '''
        i = 0
        logger.debug("get_html请求开始:" + url)
        time.sleep(random.randint(1, 10))
        logger.debug("延迟请求结束")
        while i < 3:
            try:
                html = requests.get(url=url, headers=self.headers,
                                    timeout=20).text
            except Exception:
                logger.error("重试--超时链接：" + url)
                i += 1
                html = None
        return html

    def get_elements_by_xpath(self, html, xpath):
        '''
         * @name: Tommy
         * @msg: 通过xpath获取元素对象集合
         * @param {html文本对象，xpath变量}
         * @return {element集合}
        '''
        tree = etree.HTML(html)
        element_list = tree.xpath(xpath)
        return element_list

    def get_element_value_by_xpath(self, element, xpath):
        '''
         * @name: Tommy
         * @msg: 通过xpath获取元素对象的属性值
         * @param {元素item，xpath变量}
         * @return {返回xpath固定值}
        '''
        element_value = element.xpath(xpath)
        return element_value

    def get_element_by_bs4_cssselector(self, url, css_selector):
        # 设置请求间隔
        logger.debug("get_element_by_bs4_cssselector请求开始")
        time.sleep(random.randint(1, 10) * 2)
        logger.debug("延迟请求结束")
        html = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(html, "lxml")
        txt = soup.prettify()
        print(type(txt))
        with open("html.txt", 'w', encoding='utf-8') as f:
            f.write(txt)
        # info = soup.select(css_selector)
        # print(info)