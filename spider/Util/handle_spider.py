'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-05-12 17:17:39
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-05-31 18:33:20
'''
from fake_useragent import UserAgent
from threading import Thread, Lock
from queue import Queue
from lxml import etree
import requests
from bs4 import BeautifulSoup


class HandleSpider(object):
    def __init__(self):
        '''
         * @name: Tommy
         * @msg: HandleExcel 初始化
         * @param {初始化url,headers}
         * @return {*}
        '''
        self.headers = {'User-Agent': UserAgent().random}
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
        html = requests.get(url=url, headers=self.headers).text
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
        html = requests.get(url).text
        print(html)
        soup = BeautifulSoup(html, "lxml")
        info = soup.select(css_selector)
        print(info)